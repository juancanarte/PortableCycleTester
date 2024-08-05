from django.urls import path
from cycle_test.consumers import *

ws_urlpatters = [
    path('ws/sh_read_cafe_alone/', sh_read_cafe_a.as_asgi()),
    path('ws/sh_read_cafe_1/', sh_read_cafe_1.as_asgi()),
    path('ws/sh_read_cafe_2/', sh_read_cafe_2.as_asgi()),
    path('ws/sh_read_lm_a/', sh_read_lm_a.as_asgi()),
    path('ws/sh_read_lm_1/', sh_read_lm_1.as_asgi()),
    path('ws/sh_read_lm_2/', sh_read_lm_2.as_asgi()),
    path('ws/ct_read_cafe_alone/', ct_read_cafe_a.as_asgi()),
    path('ws/ct_read_cafe_1/', ct_read_cafe_1.as_asgi()),
    path('ws/ct_read_cafe_2/', ct_read_cafe_2.as_asgi()),
]