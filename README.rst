=====
 RUN
=====

.. code:: python

   python manage.py runserver

   curl -X PUT -F "file=@/home/harry/Pictures/Selection_005.png" -F "item_id=1" http://localhost:8000/api-image/ -H "Content-Type: multipart/form-data"

   curl http://localhost:8000/api-item/\?dist\=400\&point\=-52.507629,13.1459654\&format\=json -i

=======
 Refer
=======
- http://ngee.tistory.com/965

=================
 Troubleshooting
=================
.. code:: bash

          File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/boto/s3/bucket.py", line 193, in get_key
              key, resp = self._get_key_internal(key_name, headers, query_args_l)
          File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/boto/s3/bucket.py", line 231, in _get_key_internal
              response.status, response.reason, '')
          S3ResponseError: S3ResponseError: 400 Bad Request

.. code:: python

   # seoul
   AWS_S3_HOST = 's3.ap-northeast-2.amazonaws.com'


.. code:: bash

   File "/home/harry/.virt_env/saveworld/local/lib/python2.7/site-packages/django/template/loader.py", line 25, in get_template
          raise TemplateDoesNotExist(template_name, chain=chain)
 TemplateDoesNotExist: gis/openlayers.html
 [08/Nov/2016 08:49:16] "GET /admin/core/item/1/change/ HTTP/1.1" 500 450073
