هذا برنامج حساب مواقيت الصلاة لنظام اللينكس، ويعمل أيضًا على أنظمة التشغيل الأخرى.
يعتمد هذا البرنامج على Python و GTK و مكتبة PyIslam.

# المتطلبات
- مكتبة [PyIslam](https://github.com/abougouffa/pyIslam)
- مكتبة [PyGObject](pygobject.gnome.org)
- GTK 3

# الإعدادات واللغة
- يمكن تغيير إعدادات الموقع والتفضيلات الأخرى مباشرة من ملف `main.py` اعتمادًا على [دليل PyIslam](https://github.com/abougouffa/pyIslam/blob/af664c200b3af7b92c1319301062f5a027b88887/pyIslam/praytimes.py).
- يمكن تغيير لغة عرض البرنامج من خلال استخدام `prayerNames` في `main.py`.

# إخلاء المسؤولية
هذا البرنامج يعتمد على مكتبة PyIslam لحساب مواقيت الصلاة. فلا يوجد للأسف مكتبة رسمية لهذا الأمر.