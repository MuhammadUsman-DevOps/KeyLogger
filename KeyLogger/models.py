import uuid

from django.db import models
import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files import File
from datetime import datetime


class Keys(models.Model):
    key_qr = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_title = models.CharField(max_length=1000, null=True, blank=True)
    key_notes = models.TextField(null=True, blank=True)
    qr_image = models.ImageField(upload_to='qrcode/keys')

    status = models.CharField(default="Available", max_length=50)

    def __str__(self):
        return self.key_title

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.key_qr)
        canvas = Image.new("RGB", (350, 355), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        image_name = "key-" + str(self.key_qr) + ".png"
        self.qr_image.save(image_name, File(buffer), save=False)

        img = Image.open("media/qrcode/keys/" + image_name)
        new_image = ImageDraw.Draw(img)
        myFont = ImageFont.truetype("arial.ttf", 16)

        # Add Text to an image
        new_image.text((35, 18), text=str(self.key_qr), font=myFont, fill=(0, 0, 0))

        img.save("media/qrcode/keys/" + image_name)

        canvas.close()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Keys"
        verbose_name_plural = "Keys"


class Person(models.Model):
    person_qr = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)

    qr_image = models.ImageField(upload_to='qrcode/person')

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.person_qr)
        canvas = Image.new("RGB", (350, 355), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        date = datetime.now()
        image_name = "person-" + str(self.person_qr) + ".png"
        self.qr_image.save(image_name, File(buffer), save=False)

        img = Image.open("media/qrcode/person/" + image_name)
        new_image = ImageDraw.Draw(img)
        myFont = ImageFont.truetype("arial.ttf", 16)

        # Add Text to an image
        new_image.text((35, 18), text=str(self.person_qr), font=myFont, fill=(0, 0, 0))

        img.save("media/qrcode/person/" + image_name)
        canvas.close()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Persons"
        verbose_name_plural = "Persons"


class AssignedKeys(models.Model):
    key = models.ForeignKey(Keys, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    assigned_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assigned Keys"
        verbose_name_plural = "Assigned Keys"
