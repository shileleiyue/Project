/* ================================================================
 * 所有页面组件（CDN 版，无需构建）
 * 通过 window.APP_PAGES 暴露
 * ================================================================ */
const APP_PAGES = {};

// ================= 学生端 =================
APP_PAGES.student_dashboard = {
  template: `
  <div>
    <el-row :gutter="16">
      <el-col :span="6"><div class="stat-card"><div class="label">今日学习</div><div class="value">{{ overview.today_duration_minutes || 0 }}<span class="unit">分钟</span></div></div></el-col>
      <el-col :span="6"><div class="stat-card"><div class="label">本周学习</div><div class="value">{{ overview.week_duration_minutes || 0 }}<span class="unit">分钟</span></div></div></el-col>
      <el-col :span="6"><div class="stat-card"><div class="label">累计学习资料</div><div class="value">{{ overview.total_materials || 0 }}<span class="unit">个</span></div></div></el-col>
      <el-col :span="6"><div class="stat-card"><div class="label">活跃天数</div><div class="value">{{ overview.days_active || 0 }}<span class="unit">天</span></div></div></el-col>
    </el-row>
    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="14">
        <div class="chart-box"><h3>近 7 天学习时长（分钟）</h3>
          <el-table :data="days" size="small" stripe>
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="duration_minutes" label="时长">
              <template #default="{row}">
                <el-progress :percentage="Math.min(100, row.duration_minutes/60*100)" :stroke-width="14" :text-inside="true" />
              </template>
            </el-table-column>
            <el-table-column prop="materials_count" label="资料数" width="90" />
          </el-table>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="chart-box"><h3>薄弱知识点 Top 5</h3>
          <div v-if="weak.length===0" class="empty-state"><div class="icon">📚</div>暂无错题记录</div>
          <div v-else v-for="(w,i) in weak.slice(0,5)" :key="w.id" style="padding:10px 0;border-bottom:1px dashed #eee;">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
              <span>{{i+1}}. {{w.kp_title}}</span>
              <span style="color:#f56c6c">错{{w.wrong_count}}次</span>
            </div>
            <el-progress :percentage="w.mastery_level" :status="w.mastery_level>50?'success':'exception'" />
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="chart-box" style="margin-top:16px">
      <h3>为你推荐</h3>
      <div v-if="recs.length===0" class="empty-state"><div class="icon">✨</div>暂无推荐，先去课程学习吧</div>
      <div v-else class="el-row">
        <el-col :span="8" v-for="r in recs" :key="r.id" style="padding:8px">
          <el-card shadow="hover">
            <div style="display:flex;justify-content:space-between;font-size:13px">
              <el-tag size="small" :type="r.material_type==='video'?'warning':'success'">{{r.material_type==='video'?'视频':'文档'}}</el-tag>
              <span style="color:#9ca3af">评分 {{r.score}}</span>
            </div>
            <div style="font-size:14px;font-weight:500;margin:8px 0 4px">{{r.material_title}}</div>
            <div style="font-size:12px;color:#6b7280">{{r.reason}}</div>
          </el-card>
        </el-col>
      </div>
    </div>
  </div>`,
  setup() {
    const overview = Vue.ref({});
    const days = Vue.ref([]);
    const weak = Vue.ref([]);
    const recs = Vue.ref([]);
    (async () => {
      try {
        const [o, d, w, r] = await Promise.all([
          API.get('/stats/overview'),
          API.get('/stats/daily-trend'),
          API.get('/stats/weak-points'),
          API.get('/stats/recommendations'),
        ]);
        overview.value = o.data;
        days.value = d.data.days || [];
        weak.value = w.data || [];
        recs.value = r.data.items || [];
      } catch(e){}
    })();
    return { overview, days, weak, recs };
  }
};

// ---- 课程列表（学生） ----
APP_PAGES.student_courses = {
  template: `
  <div>
    <div class="page-header"><h2>我的课程</h2>
      <el-input v-model="kw" placeholder="搜索课程" style="width:240px" clearable>
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
    </div>
    <div class="el-row">
      <el-col :span="8" v-for="c in courses" :key="c.id" style="padding:8px">
        <div class="course-card" @click="$emit('go', 'course_detail', c)">
          <div class="cover">{{c.name[0]}}</div>
          <div class="body">
            <div class="name">{{c.name}}</div>
            <div class="desc">{{c.description || '暂无简介'}}</div>
          </div>
        </div>
      </el-col>
      <el-col v-if="filtered.length===0" :span="24"><div class="empty-state"><div class="icon">📖</div>没有课程</div></el-col>
    </div>
  </div>`,
  emits: ['go'],
  setup() {
    const courses = Vue.ref([]);
    const kw = Vue.ref('');
    API.get('/courses').then(r => courses.value = r.data.results || r.data);
    const filtered = Vue.computed(() => courses.value.filter(c => !kw.value || c.name.includes(kw.value)));
    return { courses, kw, filtered, Search: ElementPlusIconsVue.Search };
  }
};

// ---- 课程详情 + 知识点树 + 资料列表 ----
APP_PAGES.course_detail = {
  template: `
  <div>
    <el-page-header @back="$emit('go','student_courses')" :content="course.name" style="margin-bottom:16px" />
    <el-row :gutter="16">
      <el-col :span="8">
        <div class="chart-box">
          <h3>知识点</h3>
          <el-tree :data="tree" node-key="id" :props="{ label: 'title', children: 'children' }"
            :expand-on-click-node="false" :default-expand-all="true"
            @node-click="onKpClick" />
        </div>
      </el-col>
      <el-col :span="16">
        <div class="chart-box">
          <h3>{{ currentKp ? '知识点：' + currentKp.title : '全部学习资料' }}</h3>
          <div v-if="materials.length===0" class="empty-state"><div class="icon">📂</div>暂无资料</div>
          <el-table v-else :data="materials" stripe>
            <el-table-column prop="title" label="标题">
              <template #default="{row}">
                <a :href="row.url || '#'" target="_blank" style="color:#409eff;text-decoration:none">{{row.title}}</a>
              </template>
            </el-table-column>
            <el-table-column label="类型" width="100">
              <template #default="{row}">
                <el-tag :type="row.material_type==='video'?'warning':'success'" size="small">
                  {{row.material_type==='video'?'视频':row.material_type==='document'?'文档':'外链'}}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="{row}">
                <el-button size="small" type="primary" link @click="openMat(row)">打开</el-button>
                <el-button size="small" type="success" link @click="markView(row)">标记学习</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>`,
  emits: ['go'],
  props: ['course'],
  setup(props) {
    const tree = Vue.ref([]);
    const materials = Vue.ref([]);
    const allMaterials = Vue.ref([]);
    const currentKp = Vue.ref(null);
    API.get(`/courses/${props.course.id}/knowledge`).then(r => tree.value = r.data.points || []);
    API.get('/materials', { params: { course: props.course.id, page_size: 100 } })
      .then(r => { allMaterials.value = r.data.results || r.data; materials.value = allMaterials.value; });
    const onKpClick = (n) => {
      currentKp.value = n;
      materials.value = allMaterials.value.filter(m => m.kp === n.id);
    };
    const openMat = (m) => {
      if (m.url) window.open(m.url, '_blank');
      else if (m.file) window.open(m.file, '_blank');
      else ElementPlus.ElMessage.warning('该资料没有可打开的链接');
    };
    const markView = (m) => {
      API.post(`/materials/${m.id}/view`, { progress_percent: 100, duration_seconds: 300, finished: true })
        .then(() => ElementPlus.ElMessage.success('已记录学习'));
    };
    return { tree, materials, currentKp, onKpClick, openMat, markView };
  }
};

// ---- 考试中心 ----
APP_PAGES.student_exams = {
  template: `
  <div>
    <div class="page-header"><h2>考试中心</h2></div>
    <el-row :gutter="16">
      <el-col :span="12" v-for="e in exams" :key="e.id">
        <el-card shadow="hover" style="margin-bottom:16px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <h3 style="margin-bottom:4px">{{e.title}}</h3>
              <div style="font-size:12px;color:#6b7280;margin-bottom:10px">
                时长 {{e.duration_minutes}} 分钟 · 满分 {{e.total_score}} · 及格 {{e.passing_score}}
              </div>
              <div style="font-size:12px;color:#9ca3af">{{e.description}}</div>
            </div>
            <el-button type="primary" @click="startExam(e)">开始考试</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col v-if="exams.length===0" :span="24"><div class="empty-state"><div class="icon">📝</div>暂无可用考试</div></el-col>
    </el-row>
    <div class="chart-box" style="margin-top:16px">
      <h3>考试记录</h3>
      <el-table :data="records" stripe>
        <el-table-column prop="exam_title" label="试卷" />
        <el-table-column label="得分">
          <template #default="{row}">
            <span :style="{color: row.is_passed?'#10b981':'#f56c6c', fontWeight:'bold'}">{{row.score || '-'}}{{row.submitted_at?' / 已提交':' (未完成)'}}</span>
          </template>
        </el-table-column>
        <el-table-column label="及格" width="80">
          <template #default="{row}">
            <el-tag v-if="row.submitted_at" :type="row.is_passed?'success':'danger'" size="small">
              {{row.is_passed?'及格':'未及格'}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="错题分析" width="120">
          <template #default="{row}">
            <el-button v-if="row.submitted_at" size="small" type="warning" link @click="showWrong(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>`,
  setup() {
    const exams = Vue.ref([]);
    const records = Vue.ref([]);
    const dialogVisible = Vue.ref(false);
    const wrongItems = Vue.ref([]);
    API.get('/exams').then(r => exams.value = r.data.results || r.data);
    API.get('/exam-records').then(r => records.value = r.data.results || r.data);
    const startExam = async (e) => {
      try {
        const { data } = await API.post(`/exams/${e.id}/start`);
        localStorage.setItem('cur_exam', JSON.stringify({ examId: e.id, recordId: data.record_id, items: data.items }));
        window.dispatchEvent(new CustomEvent('nav', { detail: { page: 'do_exam' } }));
      } catch(err) {}
    };
    const showWrong = async (r) => {
      const { data } = await API.get(`/exam-records/${r.id}/wrong/`);
      wrongItems.value = data.items;
      dialogVisible.value = true;
    };
    return { exams, records, startExam, showWrong, dialogVisible, wrongItems };
  },
  template_extra_append: false
};

// ---- 答题组件（通过事件触发） ----
APP_PAGES.do_exam = {
  template: `
  <div>
    <el-page-header @back="$emit('go','student_exams')" :content="'正在答题：' + examTitle" style="margin-bottom:16px" />
    <div style="background:#fff;border-radius:12px;padding:16px;display:flex;justify-content:space-between;margin-bottom:16px">
      <div>共 {{items.length}} 题 · 已答 {{answeredCount}} 题</div>
      <div>剩余 <span style="color:#f56c6c;font-weight:600">{{Math.max(0, Math.floor(remaining/60))}}</span> 分钟</div>
    </div>
    <div v-for="(it, idx) in items" :key="it.exam_question_id" class="quiz-card">
      <div class="q-meta">第 {{idx+1}} 题 · {{questionTypeLabel(it.question_type)}} · {{it.score}} 分</div>
      <div class="q-title">{{it.title}}</div>
      <div class="options">
        <template v-if="it.question_type==='judge'">
          <label><input type="radio" :name="'q'+it.exam_question_id" value="true" v-model="answers[it.exam_question_id]" :style="{marginRight:'8px'}" />正确</label>
          <label><input type="radio" :name="'q'+it.exam_question_id" value="false" v-model="answers[it.exam_question_id]" :style="{marginRight:'8px'}" />错误</label>
        </template>
        <template v-else-if="it.question_type==='single'">
          <label v-for="(v,k) in it.options" :key="k">
            <input type="radio" :name="'q'+it.exam_question_id" :value="k" v-model="answers[it.exam_question_id]" :style="{marginRight:'8px'}" />
            {{k}}. {{v}}
          </label>
        </template>
        <template v-else>
          <label v-for="(v,k) in it.options" :key="k">
            <input type="checkbox" :value="k" @change="(e)=>toggleMulti(it.exam_question_id, k, e.target.checked)" :style="{marginRight:'8px'}" />
            {{k}}. {{v}}
          </label>
        </template>
      </div>
    </div>
    <div style="text-align:center">
      <el-button type="primary" size="large" @click="submit">交 卷</el-button>
    </div>
  </div>`,
  emits: ['go'],
  setup() {
    const data = JSON.parse(localStorage.getItem('cur_exam') || '{}');
    const items = Vue.ref(data.items || []);
    const examId = data.examId;
    const examTitle = items.value[0] ? '试卷' : ''; // 简化
    const answers = Vue.ref({});
    const remaining = Vue.ref(data.duration_minutes ? data.duration_minutes * 60 : 1800);
    setInterval(() => remaining.value -= 1, 1000);
    const toggleMulti = (qid, val, checked) => {
      if (!Array.isArray(answers.value[qid])) answers.value[qid] = [];
      if (checked) answers.value[qid].push(val);
      else answers.value[qid] = answers.value[qid].filter(x => x !== val);
    };
    const answeredCount = Vue.computed(() => Object.keys(answers.value).length);
    const submit = async () => {
      const payload = { answers: items.value.map(it => ({
        exam_question_id: it.exam_question_id, answer: answers.value[it.exam_question_id] || null
      })) };
      if (await ElementPlus.ElMessageBox.confirm('确定交卷吗？提交后无法修改。', '提示').catch(()=>null) === null) return;
      try {
        const { data } = await API.post(`/exams/${examId}/submit`, payload);
        localStorage.removeItem('cur_exam');
        ElementPlus.ElMessage.success(`交卷成功，得分 ${data.score}/${data.total_score}`);
        window.dispatchEvent(new CustomEvent('nav', { detail: { page: 'student_exams' } }));
      } catch(e) {}
    };
    return { items, examId, examTitle, answers, remaining, toggleMulti, answeredCount, submit, questionTypeLabel };
  }
};

// ---- 错题本 ----
APP_PAGES.student_wrong = {
  template: `
  <div>
    <div class="page-header"><h2>错题本</h2></div>
    <div class="chart-box">
      <h3>薄弱知识点</h3>
      <el-tag v-for="w in weak" :key="w.id" style="margin:4px" :type="w.mastery_level<40?'danger':'warning'" effect="plain">
        {{w.kp_title}} · 错{{w.wrong_count}}次
      </el-tag>
      <div v-if="weak.length===0" class="empty-state" style="padding:24px"><div class="icon">🎉</div>暂无薄弱知识点</div>
    </div>
    <div class="chart-box">
      <h3>最近错题及相关资料</h3>
      <el-tabs v-model="tab">
        <el-tab-pane label="错题列表" name="wrong">
          <div v-if="items.length===0" class="empty-state"><div class="icon">📋</div>暂无错题</div>
          <div v-for="item in items" :key="item.question_id" class="wrong-item">
            <div class="title">[{{questionTypeLabel(item.question_type)}}] {{item.title}}</div>
            <div class="meta">正确答案：{{JSON.stringify(item.correct_answer)}} · 你的答案：{{JSON.stringify(item.student_answer)}}</div>
            <div v-if="item.analysis" class="meta" style="margin-top:6px">解析：{{item.analysis}}</div>
            <div v-if="item.related_materials?.length" style="margin-top:10px">
              <div style="font-size:12px;color:#409eff;margin-bottom:6px">📎 相关学习资料：</div>
              <el-tag v-for="rm in item.related_materials" :key="rm.id" style="margin:2px">
                <a :href="rm.url || '#'" target="_blank" style="color:inherit;text-decoration:none">{{rm.title}}</a>
              </el-tag>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>`,
  setup() {
    const weak = Vue.ref([]);
    const records = Vue.ref([]);
    const items = Vue.ref([]);
    const tab = Vue.ref('wrong');
    API.get('/stats/weak-points').then(r => weak.value = r.data || []);
    API.get('/exam-records').then(async r => {
      const recs = (r.data.results || r.data).filter(x => x.submitted_at);
      records.value = recs;
      for (const rec of recs) {
        const { data } = await API.get(`/exam-records/${rec.id}/wrong/`);
        items.value.push(...data.items);
      }
    });
    return { weak, items, tab, questionTypeLabel };
  }
};

// ---- 学习喜好分析 ----
APP_PAGES.student_preference = {
  template: `
  <div class="chart-box">
    <h3>学习喜好分析</h3>
    <el-row :gutter="16">
      <el-col :span="12">
        <h4 style="margin-bottom:10px">📚 活跃时段分布</h4>
        <div v-if="!activeHoursKeys.length" class="empty-state"><div class="icon">⏰</div>暂无数据</div>
        <div v-else v-for="h in activeHoursKeys" :key="h" style="margin-bottom:8px">
          <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px">{{h}}时</div>
          <el-progress :percentage="Math.round(pref.active_hours[h]*100)" />
        </div>
      </el-col>
      <el-col :span="12">
        <h4 style="margin-bottom:10px">🎯 学科主题权重</h4>
        <div v-if="!subjectKeys.length" class="empty-state"><div class="icon">📊</div>暂无数据</div>
        <div v-else v-for="s in subjectKeys" :key="s" style="margin-bottom:8px">
          <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px">{{s}}</div>
          <el-progress :percentage="Math.round(pref.subject_weights[s]*100)" :status="getProgressColor(s)" />
        </div>
      </el-col>
    </el-row>
    <div v-if="pref.preferred_material_type" style="margin-top:20px">
      <el-alert type="info" :closable="false" :title="'偏好资料类型：' + (pref.preferred_material_type==='video'?'视频':'文档')" />
    </div>
  </div>`,
  setup() {
    const pref = Vue.ref({});
    API.get('/stats/preferences').then(r => pref.value = r.data || {});
    const activeHoursKeys = Vue.computed(() => Object.keys(pref.value.active_hours || {}).sort());
    const subjectKeys = Vue.computed(() => Object.keys(pref.value.subject_weights || {}));
    const getProgressColor = () => '';
    return { pref, activeHoursKeys, subjectKeys, getProgressColor };
  }
};

// ---- 个人资料（学生） ----
APP_PAGES.profile_student = {
  template: `
  <div>
    <div class="chart-box">
      <h3>我的资料</h3>
      <el-form :model="form" label-width="100px" style="max-width:500px;margin-top:16px">
        <el-form-item label="学号"><el-input v-model="form.student_no" disabled /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="学院"><el-input v-model="form.college" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
        <el-form-item label="年级"><el-input v-model="form.grade" /></el-form-item>
        <el-form-item label="联系方式"><el-input v-model="form.contact" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="手机"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item><el-button type="primary" @click="save">保存</el-button></el-form-item>
      </el-form>
    </div>
    <div class="chart-box">
      <h3>我的课程成绩</h3>
      <el-table :data="scores" stripe>
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="course_name" label="课程名称" />
        <el-table-column prop="semester" label="学期" width="140" />
        <el-table-column label="成绩" width="120">
          <template #default="{row}">
            <span :style="{fontWeight:'bold', color: row.score>=60?'#10b981':'#f56c6c'}">
              {{ row.score !== null && row.score !== undefined ? row.score : '未考' }}
            </span>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="scores.length===0" class="empty-state" style="padding:20px">暂无成绩记录</div>
    </div>
  </div>`,
  setup() {
    const form = Vue.ref({});
    const scores = Vue.ref([]);
    API.get('/students/me').then(r => {
      const d = r.data; form.value = { ...d, email: d.email || d.user?.email, phone: d.phone || d.user?.phone };
    });
    API.get('/student-courses/my-scores/').then(r => scores.value = r.data || []);
    const save = async () => {
      try { await API.put('/students/me', form.value); ElementPlus.ElMessage.success('已保存'); } catch(e){}
    };
    return { form, save, scores };
  }
};

// ================= 教师端 =================
APP_PAGES.teacher_dashboard = {
  template: `
  <el-row :gutter="16">
    <el-col :span="6"><div class="stat-card"><div class="label">我教授的课程</div><div class="value">{{stats.courses || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">题库数量</div><div class="value">{{stats.questions || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">试卷数量</div><div class="value">{{stats.exams || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">资料上传</div><div class="value">{{stats.materials || 0}}</div></div></el-col>
  </el-row>`,
  setup() {
    const stats = Vue.ref({});
    const me = JSON.parse(localStorage.getItem('ls_user') || '{}');
    const tid = me.id;
    (async () => {
      const [c, q, e, m] = await Promise.all([
        API.get('/courses', { params: { teacher: tid, page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/questions', { params: { creator: tid, page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/exams', { params: { creator: tid, page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/materials', { params: { uploader: tid, page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
      ]);
      stats.value = {
        courses: c.data.count || (Array.isArray(c.data) ? c.data.length : 0),
        questions: q.data.count || 0,
        exams: e.data.count || 0,
        materials: m.data.count || 0,
      };
    })();
    return { stats };
  }
};

// ---- 课程管理（教师） ----
APP_PAGES.teacher_courses = {
  template: `
  <div>
    <div class="page-header"><h2>我的课程</h2>
      <el-button type="primary" @click="openNew">+ 新建课程</el-button>
    </div>
    <el-table :data="courses" stripe>
      <el-table-column prop="code" label="课程代码" width="120" />
      <el-table-column prop="name" label="课程名" />
      <el-table-column prop="description" label="简介" show-overflow-tooltip />
      <el-table-column label="状态" width="80">
        <template #default="{row}">
          <el-tag :type="row.is_active?'success':'info'" size="small">{{row.is_active?'启用':'停用'}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{row}">
          <el-button size="small" link @click="editKp(row)">知识点</el-button>
          <el-button size="small" link type="primary" @click="editCourse(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog.course" :title="editing?'编辑课程':'新建课程'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="代码"><el-input v-model="form.code" /></el-form-item>
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.course=false">取消</el-button>
        <el-button type="primary" @click="saveCourse">保存</el-button>
      </template>
    </el-dialog>
  </div>`,
  emits: ['go'],
  setup() {
    const courses = Vue.ref([]);
    const dialog = Vue.reactive({ course: false });
    const form = Vue.ref({ code: '', name: '', description: '' });
    const editing = Vue.ref(null);
    const refresh = () => API.get('/courses', { params: { page_size: 100 } }).then(r => courses.value = r.data.results || r.data);
    refresh();
    const openNew = () => { editing.value = null; form.value = { code: '', name: '', description: '' }; dialog.course = true; };
    const editCourse = (c) => { editing.value = c; form.value = { ...c }; dialog.course = true; };
    const saveCourse = async () => {
      try {
        if (editing.value) await API.put(`/courses/${editing.value.id}`, form.value);
        else await API.post('/courses', form.value);
        dialog.course = false; refresh(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };
    const editKp = (c) => window.dispatchEvent(new CustomEvent('nav', { detail: { page: 'teacher_kp', course: c } }));
    return { courses, dialog, form, editing, openNew, editCourse, saveCourse, editKp };
  }
};

// ---- 知识点管理 ----
APP_PAGES.teacher_kp = {
  template: `
  <div>
    <el-page-header @back="$emit('go','teacher_courses')" :content="'知识点管理：' + (course?.name||'')" style="margin-bottom:16px" />
    <el-table :data="flat" stripe row-key="id" :tree-props="{ children: 'children' }" default-expand-all>
      <el-table-column prop="title" label="知识点" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="200">
        <template #default="{row}">
          <el-button size="small" link @click="addChild(row)">+ 子节点</el-button>
          <el-button size="small" link type="primary" @click="edit(row)">编辑</el-button>
          <el-popconfirm title="确定删除？" @confirm="del(row)">
            <template #reference><el-button size="small" link type="danger">删除</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top:16px">
      <el-button type="primary" @click="addRoot">+ 新增根节点</el-button>
    </div>
    <el-dialog v-model="dialog" :title="form.id?'编辑知识点':'新增知识点'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" rows="3" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.order_no" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>`,
  emits: ['go'],
  props: ['course'],
  setup(props) {
    const tree = Vue.ref([]);
    const flat = Vue.computed(() => {
      const flatten = (list, children) => (list || []).map(n => ({ ...n, children: children(n) }));
      const build = (nodes) => flatten(nodes.map(n => build(n.children || []) ? { ...n, children: build(n.children||[]) } : n), n => []);
      return build(tree.value);
    });
    const dialog = Vue.ref(false);
    const form = Vue.ref({ title: '', description: '', order_no: 0, parent: null });
    const refresh = () => API.get(`/courses/${props.course.id}/knowledge`).then(r => tree.value = r.data.points || []);
    refresh();
    const addRoot = () => { form.value = { title: '', description: '', order_no: 0, parent: null, course: props.course.id }; dialog.value = true; };
    const addChild = (p) => { form.value = { title: '', description: '', order_no: 0, parent: p.id, course: props.course.id }; dialog.value = true; };
    const edit = (r) => { form.value = { ...r }; dialog.value = true; };
    const del = async (r) => { await API.delete(`/knowledge-points/${r.id}`); refresh(); };
    const save = async () => {
      try {
        const payload = { title: form.value.title, description: form.value.description, order_no: form.value.order_no, parent: form.value.parent, course: props.course.id };
        if (form.value.id) await API.put(`/knowledge-points/${form.value.id}`, payload);
        else await API.post('/knowledge-points', payload);
        dialog.value = false; refresh(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };
    return { tree, flat, dialog, form, addRoot, addChild, edit, del, save };
  }
};

// ---- 资料上传 ----
APP_PAGES.teacher_materials = {
  template: `
  <div>
    <div class="page-header"><h2>学习资料管理</h2>
      <el-button type="primary" @click="open">+ 上传资料</el-button>
    </div>
    <el-table :data="materials" stripe>
      <el-table-column prop="title" label="标题" />
      <el-table-column label="类型" width="100">
        <template #default="{row}">
          <el-tag :type="row.material_type==='video'?'warning':'success'" size="small">{{row.material_type}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="course_name" label="课程" />
      <el-table-column prop="kp_title" label="知识点" />
      <el-table-column prop="view_count" label="浏览" width="80" />
      <el-table-column label="操作" width="100">
        <template #default="{row}">
          <el-popconfirm title="确定删除？" @confirm="del(row)">
            <template #reference><el-button size="small" link type="danger">删除</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog" title="上传资料" width="560px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="课程">
          <el-select v-model="form.course" placeholder="选择课程" style="width:100%">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="知识点">
          <el-select v-model="form.kp" placeholder="可选" clearable style="width:100%">
            <el-option v-for="k in filteredKps" :key="k.id" :label="k.title" :value="k.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="form.material_type">
            <el-radio value="document">文档</el-radio>
            <el-radio value="video">视频</el-radio>
            <el-radio value="link">外链</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="URL / 文件">
          <el-input v-if="form.material_type==='link' || form.material_type==='video'" v-model="form.url" placeholder="填视频/文档外链" />
          <el-upload v-else :auto-upload="false" :limit="1" :on-change="onFile" drag>
            <el-icon style="font-size:28px"><UploadFilled /></el-icon>
            <div>点击或拖拽文件上传（PDF/Doc/视频等）</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>`,
  setup() {
    const materials = Vue.ref([]);
    const courses = Vue.ref([]);
    const allKps = Vue.ref([]);
    const form = Vue.ref({ course: null, kp: null, title: '', material_type: 'document', url: '', description: '' });
    const dialog = Vue.ref(false);
    const refresh = async () => {
      const [m, c] = await Promise.all([
        API.get('/materials', { params: { page_size: 200 } }),
        API.get('/courses', { params: { page_size: 200 } }),
      ]);
      materials.value = m.data.results || m.data;
      courses.value = c.data.results || c.data;
      // 简化：取所有知识点
      API.get('/knowledge-points', { params: { page_size: 500 } }).then(r => allKps.value = r.data.results || r.data);
    };
    refresh();
    const filteredKps = Vue.computed(() => allKps.value.filter(k => !form.value.course || k.course === form.value.course));
    const del = async (r) => { await API.delete(`/materials/${r.id}`); refresh(); };
    const open = () => { form.value = { course: null, kp: null, title: '', material_type: 'document', url: '', description: '' }; dialog.value = true; };
    const onFile = (file) => { form.value._file = file.raw; };
    const save = async () => {
      try {
        if (form.value._file) {
          const fd = new FormData();
          fd.append('course', form.value.course);
          if (form.value.kp) fd.append('kp', form.value.kp);
          fd.append('title', form.value.title);
          fd.append('material_type', form.value.material_type);
          fd.append('file', form.value._file);
          fd.append('description', form.value.description);
          await API.post('/materials', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
        } else {
          await API.post('/materials', form.value);
        }
        dialog.value = false; refresh(); ElementPlus.ElMessage.success('上传成功');
      } catch(e) {}
    };
    return { materials, courses, form, dialog, filteredKps, open, del, onFile, save, UploadFilled: ElementPlusIconsVue.UploadFilled };
  }
};

// ---- 题库管理 ----
APP_PAGES.teacher_questions = {
  template: `
  <div>
    <div class="page-header"><h2>题库管理</h2>
      <div>
        <el-select v-model="filterCourse" placeholder="课程" clearable style="width:160px;margin-right:8px" @change="refresh">
          <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
        <el-button type="primary" @click="open">+ 新建题目</el-button>
      </div>
    </div>
    <el-table :data="questions" stripe>
      <el-table-column prop="title" label="题干" show-overflow-tooltip />
      <el-table-column label="类型" width="90">
        <template #default="{row}">
          <el-tag size="small">{{questionTypeLabel(row.question_type)}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="70" />
      <el-table-column prop="analysis" label="解析" show-overflow-tooltip />
      <el-table-column label="操作" width="100">
        <template #default="{row}">
          <el-popconfirm title="确定删除？" @confirm="del(row)">
            <template #reference><el-button size="small" link type="danger">删除</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog" :title="editing?'编辑题目':'新建题目'" width="600px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="课程"><el-select v-model="form.course" style="width:100%"><el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" /></el-select></el-form-item>
        <el-form-item label="知识点">
          <el-select v-model="form.kp" clearable placeholder="可选" style="width:100%">
            <el-option v-for="k in filteredKps" :key="k.id" :label="k.title" :value="k.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="form.question_type">
            <el-radio value="single">单选</el-radio>
            <el-radio value="multi">多选</el-radio>
            <el-radio value="judge">判断</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="题干"><el-input v-model="form.title" type="textarea" rows="2" /></el-form-item>
        <template v-if="form.question_type !== 'judge'">
          <el-form-item label="选项">
            <div v-for="v in form.options" :key="v.k" style="display:flex;gap:6px;margin-bottom:6px">
              <el-input v-model="v.k" style="width:50px" placeholder="A" />
              <el-input v-model="v.v" placeholder="选项内容" />
              <el-button link type="danger" @click="form.options = form.options.filter(x=>x!==v)">删</el-button>
            </div>
            <el-button size="small" @click="form.options.push({k:'',v:''})">+ 选项</el-button>
          </el-form-item>
        </template>
        <el-form-item label="正确答案">
          <template v-if="form.question_type==='single'">
            <el-select v-model="form.correct_answer" style="width:120px">
              <el-option v-for="v in form.options" :key="v.k" :label="v.k" :value="v.k" />
            </el-select>
          </template>
          <template v-else-if="form.question_type==='multi'">
            <el-select v-model="form.correct_answer" multiple style="width:200px">
              <el-option v-for="v in form.options" :key="v.k" :label="v.k" :value="v.k" />
            </el-select>
          </template>
          <template v-else>
            <el-radio-group v-model="form.correct_answer_raw">
              <el-radio value="true">正确</el-radio>
              <el-radio value="false">错误</el-radio>
            </el-radio-group>
          </template>
        </el-form-item>
        <el-form-item label="解析"><el-input v-model="form.analysis" type="textarea" rows="2" /></el-form-item>
        <el-form-item label="难度"><el-input-number v-model="form.difficulty" :min="1" :max="5" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>`,
  setup() {
    const questions = Vue.ref([]);
    const courses = Vue.ref([]);
    const allKps = Vue.ref([]);
    const filterCourse = Vue.ref(null);
    const dialog = Vue.ref(false);
    const editing = Vue.ref(null);
    const form = Vue.ref({
      course: null, kp: null, question_type: 'single', title: '',
      options: [{k:'A',v:''},{k:'B',v:''},{k:'C',v:''},{k:'D',v:''}],
      correct_answer: 'A', correct_answer_raw: 'true',
      analysis: '', difficulty: 1
    });
    const refresh = async () => {
      const params = { page_size: 500 };
      if (filterCourse.value) params.course = filterCourse.value;
      const [q, c] = await Promise.all([
        API.get('/questions', { params }),
        API.get('/courses', { params: { page_size: 200 } }),
      ]);
      questions.value = q.data.results || q.data;
      courses.value = c.data.results || c.data;
      API.get('/knowledge-points', { params: { page_size: 500 } }).then(r => allKps.value = r.data.results || r.data);
    };
    refresh();
    const filteredKps = Vue.computed(() => allKps.value.filter(k => !form.value.course || k.course === form.value.course));
    const open = () => { editing.value = null; dialog.value = true; };
    const del = async (r) => { await API.delete(`/questions/${r.id}`); refresh(); };
    const save = async () => {
      const options = {};
      form.value.options.forEach(o => { if (o.k) options[o.k] = o.v; });
      let correct = form.value.correct_answer;
      if (form.value.question_type === 'judge') correct = form.value.correct_answer_raw === 'true';
      try {
        const payload = {
          course: form.value.course, kp: form.value.kp,
          question_type: form.value.question_type, title: form.value.title,
          options, correct_answer: correct,
          analysis: form.value.analysis, difficulty: form.value.difficulty,
        };
        if (editing.value) await API.put(`/questions/${editing.value.id}`, payload);
        else await API.post('/questions', payload);
        dialog.value = false; refresh(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };
    return { questions, courses, filterCourse, dialog, editing, form, refresh, filteredKps, open, del, save, questionTypeLabel };
  }
};

// ---- 试卷管理（创建 + 发布） ----
APP_PAGES.teacher_exams = {
  template: `
  <div>
    <div class="page-header"><h2>试卷管理</h2>
      <el-button type="primary" @click="open">+ 新建试卷</el-button>
    </div>
    <el-table :data="exams" stripe>
      <el-table-column prop="title" label="试卷名" />
      <el-table-column prop="course_name" label="课程" />
      <el-table-column label="状态" width="100">
        <template #default="{row}">
          <el-tag :type="row.status==='published'?'success':'info'">{{row.status==='published'?'已发布':'草稿'}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="total_score" label="总分" width="80" />
      <el-table-column label="操作" width="200">
        <template #default="{row}">
          <el-button v-if="row.status!=='published'" size="small" type="success" link @click="publish(row)">发布</el-button>
          <el-button v-else size="small" type="info" link @click="viewRecords(row)">成绩</el-button>
          <el-button size="small" link @click="edit(row)">编辑题目</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialog" :title="editing?'编辑试卷':'新建试卷'" width="720px">
      <el-form :model="form" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="试卷名"><el-input v-model="form.title" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="课程">
            <el-select v-model="form.course" style="width:100%"><el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" /></el-select>
          </el-form-item></el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="时长(分)"><el-input-number v-model="form.duration_minutes" :min="1" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="满分"><el-input-number v-model="form.total_score" :min="1" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="及格分"><el-input-number v-model="form.passing_score" :min="0" :max="100" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" rows="2" /></el-form-item>

        <el-divider>选择题目</el-divider>
        <div style="max-height:320px;overflow-y:auto;border:1px solid #eee;border-radius:8px;padding:8px">
          <div v-for="(q,i) in filteredQuestions" :key="q.id" style="padding:8px;border-bottom:1px dashed #f0f0f0;display:flex;gap:10px;align-items:center">
            <el-checkbox :model-value="selectedIds.includes(q.id)" @change="(v)=>toggleQ(q, v)">选</el-checkbox>
            <span style="flex:1;font-size:13px">{{i+1}}. [{{questionTypeLabel(q.question_type)}}] {{q.title}}</span>
            <el-input-number v-if="selectedIds.includes(q.id)" size="small" :value="scores[q.id]" @update:model-value="v => scores[q.id]=v" style="width:80px" />
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <!-- 成绩弹窗 -->
    <el-dialog v-model="recDialog" title="考试成绩" width="640px">
      <el-table :data="records" stripe>
        <el-table-column prop="student_name" label="学生" />
        <el-table-column label="得分">
          <template #default="{row}">
            <span :style="{color: row.is_passed?'#10b981':'#f56c6c', fontWeight:'bold'}">{{row.score}}</span>
          </template>
        </el-table-column>
        <el-table-column label="及格" width="80">
          <template #default="{row}">
            <el-tag :type="row.is_passed?'success':'danger'" size="small">{{row.is_passed?'及格':'未及格'}}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>`,
  setup() {
    const exams = Vue.ref([]);
    const courses = Vue.ref([]);
    const allQuestions = Vue.ref([]);
    const dialog = Vue.ref(false);
    const editing = Vue.ref(null);
    const form = Vue.ref({ title: '', course: null, description: '', duration_minutes: 30, total_score: 100, passing_score: 60 });
    const selectedIds = Vue.ref([]);
    const scores = Vue.ref({});
    const recDialog = Vue.ref(false);
    const records = Vue.ref([]);

    const refresh = async () => {
      const [e, c, q] = await Promise.all([
        API.get('/exams', { params: { page_size: 200 } }),
        API.get('/courses', { params: { page_size: 200 } }),
        API.get('/questions', { params: { page_size: 500 } }),
      ]);
      exams.value = e.data.results || e.data;
      courses.value = c.data.results || c.data;
      allQuestions.value = q.data.results || q.data;
    };
    refresh();
    const filteredQuestions = Vue.computed(() => allQuestions.value.filter(q => !form.value.course || q.course === form.value.course));
    const toggleQ = (q, v) => {
      if (v) { selectedIds.value.push(q.id); scores.value[q.id] = 20; }
      else { selectedIds.value = selectedIds.value.filter(x => x !== q.id); delete scores.value[q.id]; }
    };
    const open = () => { editing.value = null; selectedIds.value = []; scores.value = {}; dialog.value = true; };
    const publish = async (e) => { await API.post(`/exams/${e.id}/publish`); refresh(); ElementPlus.ElMessage.success('已发布'); };
    const viewRecords = async (e) => {
      const { data } = await API.get(`/exams/${e.id}/records`);
      const list = data.results || data;
      records.value = await Promise.all(list.map(async r => {
        try {
          const s = await API.get(`/students/${r.student}/`);
          return { ...r, student_name: s.data.name || s.data.student_no };
        } catch { return { ...r, student_name: r.student }; }
      }));
      recDialog.value = true;
    };
    const save = async () => {
      try {
        const items = selectedIds.value.map((qid, i) => ({ question_id: qid, score: scores.value[qid], order_no: i+1 }));
        if (editing.value) {
          // 简化：删除重建 items
          await API.delete(`/exams/${editing.value.id}/`);
        }
        await API.post('/exams', { ...form.value, items });
        dialog.value = false; refresh(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };
    const edit = (e) => { editing.value = e; form.value = { title: e.title, course: e.course, description: e.description, duration_minutes: e.duration_minutes, total_score: e.total_score, passing_score: e.passing_score }; selectedIds.value = (e.items || []).map(x => x.question_id); scores.value = {}; (e.items || []).forEach(x => scores.value[x.question_id] = x.score); dialog.value = true; };
    return { exams, courses, allQuestions, dialog, editing, form, selectedIds, scores, filteredQuestions, refresh, open, toggleQ, publish, viewRecords, save, edit, recDialog, records, questionTypeLabel };
  }
};

// ================= 管理员端 =================
APP_PAGES.admin_dashboard = {
  template: `
  <el-row :gutter="16">
    <el-col :span="6"><div class="stat-card"><div class="label">学生总数</div><div class="value">{{stats.students || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">教师总数</div><div class="value">{{stats.teachers || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">课程总数</div><div class="value">{{stats.courses || 0}}</div></div></el-col>
    <el-col :span="6"><div class="stat-card"><div class="label">注册账号</div><div class="value">{{stats.users || 0}}</div></div></el-col>
  </el-row>`,
  setup() {
    const stats = Vue.ref({});
    (async () => {
      const [s, t, c, u] = await Promise.all([
        API.get('/students', { params: { page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/teachers', { params: { page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/courses', { params: { page_size: 1 } }).catch(() => ({ data: { count: 0 } })),
        API.get('/students', { params: { page_size: 1 } }).catch(() => ({ data: { count: 0 } })), // 简化
      ]);
      stats.value = {
        students: s.data.count || 0, teachers: t.data.count || 0,
        courses: c.data.count || 0, users: (s.data.count || 0) + (t.data.count || 0) + 1,
      };
    })();
    return { stats };
  }
};

// ---- 学生管理 CRUD ----
APP_PAGES.admin_students = {
  template: `
  <div>
    <el-tabs v-model="activeTab">
      <!-- ===== Tab 1：学生信息 CRUD ===== -->
      <el-tab-pane label="学生信息管理" name="students">
        <div class="page-header" style="margin-top:16px">
          <div class="page-title" style="font-size:16px;font-weight:600">学生信息（姓名/学号/联系方式/学院/专业/年级）</div>
          <div>
            <el-input v-model="kw" placeholder="学号/姓名" style="width:200px;margin-right:8px" clearable />
            <el-button type="primary" @click="open">+ 新增学生</el-button>
          </div>
        </div>
        <el-table :data="filtered" stripe>
          <el-table-column prop="student_no" label="学号" width="120" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="college" label="学院" />
          <el-table-column prop="major" label="专业" />
          <el-table-column prop="grade" label="年级" width="90" />
          <el-table-column prop="contact" label="联系方式" />
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" link @click="edit(row)">编辑</el-button>
              <el-popconfirm title="确定删除？" @confirm="del(row)">
                <template #reference><el-button size="small" link type="danger">删除</el-button></template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ===== Tab 2：成绩管理 ===== -->
      <el-tab-pane label="学生课程成绩" name="scores">
        <div class="page-header" style="margin-top:16px">
          <div class="page-title" style="font-size:16px;font-weight:600">学生选课成绩（管理员可增删改查）</div>
          <el-button type="primary" @click="openScore">+ 新增成绩</el-button>
        </div>
        <el-table :data="scores" stripe>
          <el-table-column prop="student_no" label="学号" width="110" />
          <el-table-column prop="student_name" label="姓名" width="100" />
          <el-table-column prop="course_code" label="课程代码" width="110" />
          <el-table-column prop="course_name" label="课程名称" />
          <el-table-column prop="semester" label="学期" width="140" />
          <el-table-column label="成绩" width="100">
            <template #default="{row}">
              <span :style="{fontWeight:'bold', color: row.score>=60?'#10b981':'#f56c6c'}">
                {{ row.score !== null ? row.score : '未考' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140">
            <template #default="{row}">
              <el-button size="small" link @click="editScore(row)">编辑</el-button>
              <el-popconfirm title="确定删除？" @confirm="delScore(row)">
                <template #reference><el-button size="small" link type="danger">删除</el-button></template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- 学生 dialog -->
    <el-dialog v-model="dialog" :title="editing?'编辑学生':'新增学生'" width="520px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="学号"><el-input v-model="form.student_no" :disabled="!!editing" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="学院"><el-input v-model="form.college" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
        <el-form-item label="年级"><el-input v-model="form.grade" /></el-form-item>
        <el-form-item label="联系方式"><el-input v-model="form.contact" /></el-form-item>
        <template v-if="!editing">
          <el-divider>创建账号</el-divider>
          <el-form-item label="用户名"><el-input v-model="form.username" placeholder="登录用户名" /></el-form-item>
          <el-form-item label="初始密码"><el-input v-model="form.password" placeholder="默认 123456" /></el-form-item>
          <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
          <el-form-item label="手机"><el-input v-model="form.phone" /></el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <!-- 成绩 dialog -->
    <el-dialog v-model="scoreDialog" :title="editingScore?'编辑成绩':'新增成绩'" width="480px">
      <el-form :model="scoreForm" label-width="80px">
        <el-form-item label="学生">
          <el-select v-model="scoreForm.student" style="width:100%" placeholder="选择学生">
            <el-option v-for="s in students" :key="s.id" :label="s.student_no + ' ' + s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程">
          <el-select v-model="scoreForm.course" style="width:100%" placeholder="选择课程">
            <el-option v-for="c in courses" :key="c.id" :label="c.code + ' ' + c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="成绩"><el-input-number v-model="scoreForm.score" :min="0" :max="100" :step="0.5" style="width:100%" /></el-form-item>
        <el-form-item label="学期"><el-input v-model="scoreForm.semester" placeholder="如 2025-2026-1" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="scoreDialog=false">取消</el-button>
        <el-button type="primary" @click="saveScore">保存</el-button>
      </template>
    </el-dialog>
  </div>`,
  setup() {
    const activeTab = Vue.ref('students');
    const students = Vue.ref([]);
    const courses = Vue.ref([]);
    const scores = Vue.ref([]);
    const kw = Vue.ref('');
    const dialog = Vue.ref(false);
    const editing = Vue.ref(null);
    const form = Vue.ref({ student_no: '', name: '', college: '', major: '', grade: '', contact: '', username: '', password: '123456', email: '', phone: '' });
    const scoreDialog = Vue.ref(false);
    const editingScore = Vue.ref(null);
    const scoreForm = Vue.ref({ student: null, course: null, score: null, semester: '' });

    const refresh = async () => {
      const [s, c] = await Promise.all([
        API.get('/students', { params: { page_size: 500 } }),
        API.get('/courses', { params: { page_size: 200 } }),
      ]);
      students.value = s.data.results || s.data;
      courses.value = c.data.results || c.data;
    };
    const refreshScores = () => API.get('/student-courses/', { params: { page_size: 500 } }).then(r => scores.value = r.data.results || r.data);
    refresh(); refreshScores();

    const filtered = Vue.computed(() => students.value.filter(s => !kw.value || s.student_no.includes(kw.value) || s.name.includes(kw.value)));
    const open = () => { editing.value = null; dialog.value = true; };
    const edit = (r) => { editing.value = r; form.value = { ...r }; dialog.value = true; };
    const del = async (r) => { await API.delete(`/students/${r.id}`); refresh(); ElementPlus.ElMessage.success('已删除'); };
    const save = async () => {
      try {
        if (editing.value) { await API.put(`/students/${editing.value.id}`, form.value); }
        else { await API.post('/students', form.value); }
        dialog.value = false; refresh(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };

    const openScore = () => { editingScore.value = null; scoreForm.value = { student: null, course: null, score: null, semester: '' }; scoreDialog.value = true; };
    const editScore = (r) => { editingScore.value = r; scoreForm.value = { student: r.student, course: r.course, score: r.score, semester: r.semester }; scoreDialog.value = true; };
    const delScore = async (r) => { await API.delete(`/student-courses/${r.id}`); refreshScores(); ElementPlus.ElMessage.success('已删除'); };
    const saveScore = async () => {
      try {
        if (editingScore.value) { await API.put(`/student-courses/${editingScore.value.id}`, scoreForm.value); }
        else { await API.post('/student-courses/', scoreForm.value); }
        scoreDialog.value = false; refreshScores(); ElementPlus.ElMessage.success('保存成功');
      } catch(e) {}
    };

    return { activeTab, students, courses, scores, kw, dialog, editing, form, filtered, open, edit, del, save,
             scoreDialog, editingScore, scoreForm, openScore, editScore, delScore, saveScore };
  }
};

// ===== 注册所有页面 =====
Object.entries(APP_PAGES).forEach(([name, comp]) => {
  comp.name = name;
});
window.APP_PAGES = APP_PAGES;
