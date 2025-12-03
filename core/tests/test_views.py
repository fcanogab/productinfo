from django.test import TestCase
from django.urls import reverse
from core.models import Software, Feature, Activity, Threat, Campaign

########################################################
####### Start Test List views ##########################
########################################################

class SoftwareListViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/software/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/software_list.html')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('software_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('software_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/software_list.html')

class FeatureListViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/features/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feature_list.html')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('feature_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('feature_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feature_list.html')

class ThreatListViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/threats/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/threat_list.html')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('threat_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('threat_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/threat_list.html')

class CampaignListViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/campaigns/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/campaign_list.html')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('campaign_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('campaign_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/campaign_list.html')

class StandardListViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/standards/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/standard_list.html')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('standard_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('standard_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/standard_list.html')

########################################################
####### End Test List views ############################
########################################################

########################################################
####### Start Test Detail views ########################
########################################################

class SoftwareDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.software = Software.objects.create(
            name='Red Hat Enterprise Linux',
            description='Red Hat Enterprise Linux is a Linux distribution developed by Red Hat. It is the foundation for Red Hat Enterprise Linux and other Red Hat products.',
        )

    def test_view_detail_software_exists(self):
        response = self.client.get(f'/software/{self.software.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/software_detail.html')

class FeatureDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feature = Feature.objects.create(
            name='Confidential Computing',
            description='Confidential Computing is a technology that allows data to be processed in a secure and confidential manner.',
        )

    def test_view_detail_feature_exists(self):
        response = self.client.get(f'/features/{self.feature.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feature_detail.html')

class ActivityDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.activity = Activity.objects.create(
            name='Security Architecture Review (SAR)',
            description='The Security Architecture Review (SAR) is a process that reviews the security architecture of a system to ensure it is secure and compliant with security policies and standards.',
        )
    
    def test_view_detail_activity_exists(self):
        response = self.client.get(f'/activities/{self.activity.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/activity_detail.html')

class ThreatDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.threat = Threat.objects.create(
            name='Data Leakage',
            description='Data Leakage is the unauthorized disclosure of sensitive data.',
        )
    
    def test_view_detail_threat_exists(self):
        response = self.client.get(f'/threats/{self.threat.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/threat_detail.html')

class CampaignDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.campaign = Campaign.objects.create(
            name='All components with a SAR',
            description='All components with a SAR activity',
        )
    
    def test_view_detail_campaign_exists(self):
        response = self.client.get(f'/campaigns/{self.campaign.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/campaign_detail.html')
