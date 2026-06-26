"""analytics 视图：学习强度/学习情况/学习喜好/推荐"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, date, datetime

from .models import WeakKP, DailyStat, LearningPreference, Recommendation
from .serializers import (
    WeakKPSerializer, DailyStatSerializer,
    LearningPreferenceSerializer, RecommendationSerializer,
)
from accounts.permissions import IsStudent


def _build_weekly_stats(student):
    """根据 MaterialView 记录生成近 7 天每日统计"""
    from materials.models import MaterialView
    today = date.today()
    days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        qs = MaterialView.objects.filter(student=student, started_at__date=d)
        dur = qs.aggregate(s=Sum('duration_seconds')).get('s') or 0
        m_count = qs.values('material').distinct().count()
        k_count = qs.values('material__kp').distinct().count()
        finished = qs.filter(finished=True).count()
        started = qs.count()
        rate = round(finished / started, 2) if started else 0
        days.append({
            'date': d.isoformat(),
            'duration_seconds': dur,
            'duration_minutes': round(dur / 60, 1),
            'materials_count': m_count,
            'kps_count': k_count,
            'finish_rate': rate,
        })
    return days


def _build_preference(student):
    """根据历史学习行为推断学习喜好"""
    from materials.models import MaterialView
    qs = MaterialView.objects.filter(student=student).select_related('material')
    total = qs.count()
    if total == 0:
        return {'preferred_material_type': '', 'active_hours': {}, 'subject_weights': {}}

    # 资料类型偏好
    type_counter = {}
    for mv in qs:
        t = mv.material.material_type
        type_counter[t] = type_counter.get(t, 0) + 1
    preferred_type = max(type_counter, key=type_counter.get) if type_counter else ''

    # 活跃时段
    hour_counter = {}
    for mv in qs:
        h = mv.started_at.hour
        hour_counter[h] = hour_counter.get(h, 0) + 1
    max_h = max(hour_counter.values()) or 1
    active_hours = {str(h): round(c / max_h, 2) for h, c in hour_counter.items()}

    # 主题权重（按课程名称聚合）
    subject_counter = {}
    for mv in qs.select_related('material__course'):
        cn = mv.material.course.name
        subject_counter[cn] = subject_counter.get(cn, 0) + 1
    max_s = max(subject_counter.values()) or 1
    subject_weights = {s: round(c / max_s, 2) for s, c in subject_counter.items()}

    pref, _ = LearningPreference.objects.get_or_create(student=student)
    pref.preferred_material_type = preferred_type
    pref.active_hours = active_hours
    pref.subject_weights = subject_weights
    pref.save()

    return {
        'preferred_material_type': preferred_type,
        'active_hours': active_hours,
        'subject_weights': subject_weights,
    }


def _build_overview(student):
    """学习强度总览"""
    from materials.models import MaterialView
    now = timezone.now()
    today_start = datetime.combine(now.date(), datetime.min.time(), tzinfo=now.tzinfo)
    week_start = today_start - timedelta(days=now.weekday())

    today_qs = MaterialView.objects.filter(student=student, started_at__gte=today_start)
    week_qs = MaterialView.objects.filter(student=student, started_at__gte=week_start)
    all_qs = MaterialView.objects.filter(student=student)

    today_dur = (today_qs.aggregate(s=Sum('duration_seconds')).get('s') or 0)
    week_dur = (week_qs.aggregate(s=Sum('duration_seconds')).get('s') or 0)
    total_dur = (all_qs.aggregate(s=Sum('duration_seconds')).get('s') or 0)

    return {
        'today_duration_minutes': round(today_dur / 60, 1),
        'week_duration_minutes': round(week_dur / 60, 1),
        'total_duration_minutes': round(total_dur / 60, 1),
        'today_materials': today_qs.values('material').distinct().count(),
        'week_materials': week_qs.values('material').distinct().count(),
        'total_materials': all_qs.values('material').distinct().count(),
        'days_active': all_qs.datetimes('started_at', 'day').distinct().count(),
    }


def _build_recommendations(student):
    """生成推荐：优先推荐薄弱知识点下未看过的资料"""
    from materials.models import Material
    weak_list = WeakKP.objects.filter(student=student).order_by('-wrong_count')[:10]
    seen_ids = set(student.material_views.values_list('material_id', flat=True))
    recs = []
    for wk in weak_list:
        mats = Material.objects.filter(
            kp=wk.kp
        ).exclude(id__in=seen_ids).order_by('-view_count')[:3]
        for m in mats:
            score = wk.wrong_count * 10 + wk.mastery_level
            recs.append({
                'material': m,
                'reason': f'你在知识点「{wk.kp.title}」上错题 {wk.wrong_count} 次，建议复习',
                'score': score,
            })
    recs.sort(key=lambda x: x['score'], reverse=True)

    Recommendation.objects.filter(student=student).delete()
    out = []
    for r in recs[:10]:
        rec = Recommendation.objects.create(
            student=student, material=r['material'], reason=r['reason'], score=r['score']
        )
        out.append(RecommendationSerializer(rec).data)
    return out


class AnalyticsViewSet(viewsets.GenericViewSet):
    """学习分析（仅学生本人）"""
    permission_classes = [IsStudent]

    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """学习强度总览"""
        return Response(_build_overview(request.user))

    @action(detail=False, methods=['get'], url_path='daily-trend')
    def daily_trend(self, request):
        """近 7 天学习时长曲线"""
        return Response({'days': _build_weekly_stats(request.user)})

    @action(detail=False, methods=['get'], url_path='weak-points')
    def weak_points(self, request):
        """薄弱知识点列表"""
        qs = WeakKP.objects.filter(student=request.user).order_by('-wrong_count', 'mastery_level')
        return Response(WeakKPSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='preferences')
    def preferences(self, request):
        """学习喜好分析"""
        data = _build_preference(request.user)
        return Response(data)

    @action(detail=False, methods=['get'], url_path='recommendations')
    def recommendations(self, request):
        """推荐学习资料"""
        return Response({'items': _build_recommendations(request.user)})
