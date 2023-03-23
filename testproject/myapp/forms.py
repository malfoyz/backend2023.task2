from django.forms import (
    modelform_factory,
    ModelForm,
)

from .models import User

# 1. с помощью фабрики классов
# UserForm = modelform_factory(
#     model=User,
#     fields='__all__'
# )

# 2. путем быстрого объявления
class UserForm(ModelForm):
    """Форма, связанная с моделью пользователя"""

    class Meta:
        model = User
        fields = '__all__'