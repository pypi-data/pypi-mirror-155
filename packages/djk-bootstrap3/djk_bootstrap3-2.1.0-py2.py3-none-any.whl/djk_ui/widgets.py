from django.forms.widgets import ChoiceWidget


class UiBaseGridWidget(ChoiceWidget):

    js_classpath = 'FkGridWidget'
    template_id = 'ko_fk_grid_widget'
    component_template_str = '<span{component_attrs}></span>'
