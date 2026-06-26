from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Work, Chapter, OutlineNode, DailyStats, Category, Tag, Character, Relationship, TimelineEvent, TechNode

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.work = Work.objects.create(title='测试作品', description='测试描述', user=self.user)
        self.chapter = Chapter.objects.create(title='测试章节', content='测试内容', work=self.work, order=1)

    def test_work_creation(self):
        self.assertEqual(self.work.title, '测试作品')
        self.assertEqual(self.work.user, self.user)
        self.assertFalse(self.work.is_deleted)

    def test_work_soft_delete(self):
        self.work.delete()
        self.work.refresh_from_db()
        self.assertTrue(self.work.is_deleted)

    def test_chapter_creation(self):
        self.assertEqual(self.chapter.title, '测试章节')
        self.assertEqual(self.chapter.work, self.work)

    def test_chapter_ordering(self):
        ch2 = Chapter.objects.create(title='第二章', work=self.work, order=2)
        chapters = self.work.chapters.all()
        self.assertEqual(chapters[0].order, 1)
        self.assertEqual(chapters[1].order, 2)

    def test_outline_node_creation(self):
        node = OutlineNode.objects.create(title='大纲节点', work=self.work)
        self.assertEqual(node.title, '大纲节点')
        self.assertEqual(node.work, self.work)

    def test_daily_stats_creation(self):
        from datetime import date
        stats = DailyStats.objects.create(date=date.today(), word_count=500, duration_seconds=1800)
        self.assertEqual(stats.word_count, 500)

    def test_category_creation(self):
        cat = Category.objects.create(name='玄幻')
        self.assertEqual(str(cat), '玄幻')

    def test_tag_creation(self):
        tag = Tag.objects.create(name='热门')
        self.assertEqual(str(tag), '热门')

    def test_work_category_and_tags(self):
        cat = Category.objects.create(name='玄幻')
        tag = Tag.objects.create(name='热门')
        self.work.category = cat
        self.work.save()
        self.work.tags.add(tag)
        self.assertEqual(self.work.category, cat)
        self.assertIn(tag, self.work.tags.all())

    def test_character_creation(self):
        char = Character.objects.create(name='张三', work=self.work)
        self.assertEqual(str(char), '张三')
        self.assertEqual(char.work, self.work)

    def test_character_soft_delete(self):
        char = Character.objects.create(name='李四', work=self.work)
        char.delete()
        char.refresh_from_db()
        self.assertTrue(char.is_deleted)

    def test_relationship_creation(self):
        char1 = Character.objects.create(name='角色A', work=self.work)
        char2 = Character.objects.create(name='角色B', work=self.work)
        rel = Relationship.objects.create(character1=char1, character2=char2, relation_type='朋友')
        self.assertEqual(str(rel), '角色A - 角色B : 朋友')

    def test_timeline_event_creation(self):
        char = Character.objects.create(name='角色C', work=self.work)
        event = TimelineEvent.objects.create(title='重要事件', date='2026-01-01', work=self.work)
        event.characters.add(char)
        self.assertEqual(event.title, '重要事件')
        self.assertIn(char, event.characters.all())

    def test_tech_node_creation(self):
        parent = TechNode.objects.create(name='父节点', work=self.work)
        child = TechNode.objects.create(name='子节点', parent=parent, work=self.work)
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.work = Work.objects.create(title='测试作品', description='测试描述', user=self.user)

    def test_login_required_redirect(self):
        response = self.client.get(reverse('work_list'))
        self.assertRedirects(response, '/login/?next=/')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('work_list'))

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_work_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('work_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试作品')

    def test_work_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('work_create'), {'title': '新作品', 'description': '新描述'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Work.objects.filter(title='新作品').exists())

    def test_work_detail(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('work_detail', args=[self.work.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试作品')

    def test_work_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('work_delete', args=[self.work.id]))
        self.assertEqual(response.status_code, 302)
        self.work.refresh_from_db()
        self.assertTrue(self.work.is_deleted)

    def test_work_isolation(self):
        other_user = User.objects.create_user(username='other', password='otherpass123')
        other_work = Work.objects.create(title='其他人的作品', user=other_user)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('work_list'))
        self.assertContains(response, '测试作品')
        self.assertNotContains(response, '其他人的作品')

    def test_export_txt(self):
        Chapter.objects.create(title='第一章', content='第一章内容', work=self.work, order=1)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('export_work_txt', args=[self.work.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('测试作品', response.content.decode('utf-8'))
        self.assertIn('第一章内容', response.content.decode('utf-8'))

    def test_export_json(self):
        Chapter.objects.create(title='第一章', content='第一章内容', work=self.work, order=1)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('export_work_json', args=[self.work.id]))
        self.assertEqual(response.status_code, 200)
        import json
        data = json.loads(response.content)
        self.assertEqual(data['title'], '测试作品')
        self.assertEqual(len(data['chapters']), 1)