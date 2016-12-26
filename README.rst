=====
 RUN
=====

.. code:: python

   python manage.py runserver

   curl -X PUT -F "file=@/home/harry/Pictures/Selection_005.png" -F "item_id=1" http://localhost:8000/api-image/ -H "Content-Type: multipart/form-data"

- api call with geometry params

.. code:: python

   curl http://localhost:8000/api-item/?dist=400&point=-52.507629,13.1459654&format=json -i

=========
Reference
=========
- http://ngee.tistory.com/965

=================
 Troubleshooting
=================
- States of Item

.. code:: bash
생성 : created

진행중 : ongoing

완료 : completed

.. code:: bash

   Web configuration in Elastic Beanstalk

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

- S3ResponseError: S3ResponseError: 400 Bad Request

.. code:: bash

          File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/boto/s3/bucket.py", line 193, in get_key
              key, resp = self._get_key_internal(key_name, headers, query_args_l)
          File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/boto/s3/bucket.py", line 231, in _get_key_internal
              response.status, response.reason, '')
          S3ResponseError: S3ResponseError: 400 Bad Request

.. code:: python

   # seoul
   AWS_S3_HOST = 's3.ap-northeast-2.amazonaws.com'


- gis/openlayers.html

.. code:: bash

   File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/django/template/loader.py", line 25, in get_template
          raise TemplateDoesNotExist(template_name, chain=chain)
 TemplateDoesNotExist: gis/openlayers.html
 [08/Nov/2016 08:49:16] "GET /admin/core/item/1/change/ HTTP/1.1" 500 450073

.. code:: python

   INSTALLED_APPS = [
   ...
   'rest_framework_gis',
   ...
   ]

- Yum does not have libjpeg-devel-6b available for installation

https://www.cocept.io/blog/development/using-pillow-on-amazon-elastic-beanstalk/

- Django static files not working on elastic beanstalk

.. code:: python

    option_settings:
      aws:elasticbeanstalk:application:environment:
        DJANGO_SETTINGS_MODULE: "main.settings"
        PYTHONPATH: "/opt/python/current/app/main:$PYTHONPATH"
      aws:elasticbeanstalk:container:python:
        WSGIPath: main/wsgi.py
      aws:elasticbeanstalk:container:python:staticfiles:
        "/static/": "static/"
- No 'Access-Control-Allow-Origin' header is present on the requested resource

https://github.com/ottoyiu/django-cors-headers




- new bucket, www.healworld.co.kr
