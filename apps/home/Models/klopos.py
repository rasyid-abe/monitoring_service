from django.db import models

class MCMSMenuRetina(models.Model):
    id_m_cms_menu = models.IntegerField(primary_key=True)
    m_cms_menu_name = models.TextField()
    m_cms_menu_english_name = models.TextField()
    m_cms_menu_id_parent = models.IntegerField()
    m_cms_menu_controller = models.TextField()
    m_cms_menu_function = models.TextField()
    m_cms_menu_url = models.TextField()
    m_cms_menu_is_menu = models.IntegerField()
    m_cms_menu_is_menu_android = models.IntegerField()
    m_cms_menu_is_golang = models.IntegerField()
    m_cms_menu_icon_src = models.TextField()
    m_cms_menu_premium = models.IntegerField()
    m_cms_menu_seq = models.IntegerField()
    is_android_transactional = models.IntegerField()
    is_have_view = models.IntegerField()
    is_have_create = models.IntegerField()
    is_have_update = models.IntegerField()
    is_have_void = models.IntegerField()
    is_have_delete = models.IntegerField()
    is_menu_mobile = models.IntegerField()
    Page_Banner_id_page_banner = models.IntegerField()
    createdby = models.IntegerField()
    createdate = models.DateTimeField()
    updateby = models.IntegerField()
    updatedate = models.DateTimeField()
    active_status = models.IntegerField()
    menu_type = models.IntegerField()
    menu_alias = models.TextField()

    class Meta:
        managed = False
        db_table = 'M_CMS_Menu_Retina'
