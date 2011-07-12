# Enable request object in all template renderers
TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.request",
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  'helpers.loginout_url',
  )


