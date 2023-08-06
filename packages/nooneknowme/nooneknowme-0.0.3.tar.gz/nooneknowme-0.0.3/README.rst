แพกเกจสร้างมาเล่นๆ”
===================

PyPi: https://pypi.org/project/nooneknowme/

นั่งเรียนเลยทำขึ้นมาเล่นๆ เปิดเพลงที่ชอบ และ มี ascii art

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install nooneknowme

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   from nooneknowme import Nooneknowme

   testname = Nooneknowme()#ชื่อคลาส
   testname.show_name()#แนะนำตัว
   testname.about()#เขียนเล่น
   testname.picasciiart()#พิคอาร์ท
   testname.playmusic()# ลิ้งเพลงที่ชอบ
