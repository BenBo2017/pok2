from django.db import models
from djgeojson.fields import PointField as jgeoPointField

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
import datetime, pytz


DEFAULT_ID = 1

#Receiver fuer den Default-Staff  Haken
@receiver(pre_save, sender=User)
def set_new_user_staff(sender, instance, **kwargs):
    if instance._state.adding is True:
        print("Creating Staff User")
        instance.is_staff = True
    
class KundenAdmin(models.Model):
    Kundennummer = models.IntegerField(null=True)
    LizenzExpire = models.DateField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=DEFAULT_ID)
    
    def __str__(self):
        return 'KN: ' + str(self.Kundennummer)
    
    class Meta:
        verbose_name_plural = "Kunden"
        verbose_name ="Kunde"        

class Messung(models.Manager):
    
    def createWert(self, instr):
        #Create Messwert from stringInput
        serial = instr[:4]
        sonde = Sonde.objects.get(Serial = serial)
        #Konstanten laden
        rmt = instr[4:8]
        rm1 = instr[8:10]
        rm2 = instr[10:12]
        #Felder fuer Messwert erzeugen
        #idx = len(Messwert.objects.all())+1
        dt = datetime.datetime(2001, 1, 1, tzinfo=pytz.UTC) + datetime.timedelta(seconds = int(rmt))
        temp = sonde.K2_temp-(65000.-float(rm1))/65000.*(sonde.K2_temp-sonde.K1_temp)
        pres = sonde.K2_pres-(65000.-float(rm2))/65000.*(sonde.K2_pres-sonde.K1_pres)
        geom = sonde.geom
        #Messung in Datenbank hinterlegen
        wert = self.create(Serial = sonde, Date = dt, Temperature = temp, Pressure = pres, geom = geom)#, ID = idx)
        
        return wert

class Sonde(models.Model):
    Serial = models.CharField(max_length=16)
    Date = models.DateTimeField('date measured', null=True)
    geom = jgeoPointField(null=True)
    picture = models.ImageField(null=True)
    owned_by = models.ForeignKey(KundenAdmin, on_delete=models.CASCADE,default=DEFAULT_ID)   
    
    K1_temp = models.FloatField(null=True)
    K2_temp = models.FloatField(null=True)
    K1_pres = models.FloatField(null=True)
    K2_pres = models.FloatField(null=True)
    
    class Meta:
        verbose_name_plural = "Sonden"
        verbose_name = "Sonde"
        
    def __str__(self):
        return 'Sonde: ' + self.Serial
        
        
    @property
    def popupContent(self):
        return '<img src="{}" class=popupImage /> <p> Serial: {} </p>'.format(self.picture.url,self.Serial)
    
class Messwert(models.Model):
    Serial = models.ForeignKey(Sonde, on_delete=models.CASCADE)
    Serialnumber = models.CharField(max_length=16, null=True, blank=True)
    Date = models.DateTimeField()
    Temperature = models.FloatField()
    Pressure = models.FloatField()
    #geom = jgeoPointField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Messwerte"
        verbose_name = "Messwert"

    def __str__(self):
        return 'Sonde: ' + self.Serial.Serial + ' Date: ' + str(self.Date)
    
    @property
    def popupContent(self):
        return 'Measured: {} <p> Serial: {} </p> <img src="{}" class=popupImage /> <p>'.format(self.Date,self.Serial.Serial,self.Serial.picture.url)
    
    def save(self,*args,**kwargs):
        self.geom = self.Serial.geom
        self.Serialnumber = self.Serial.Serial
        
        super(Messwert,self).save(*args, **kwargs)
    
    #Automatische Erzeugung durch Sonde    
    objects = Messung()

   
    
class Nutzer(models.Model):
    KundenAdmin = models.ForeignKey(KundenAdmin, on_delete = models.CASCADE,default=DEFAULT_ID)
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=DEFAULT_ID)
    Name = models.CharField(max_length=16)
    
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.username != 'admin':
            Nutzer.objects.create(user=instance)
    #@receiver(post_save, sender=User)
    #def save_user_profile(sender, instance, **kwargs):
    #    instance.nutzer.save()
   

    class Meta:
        verbose_name_plural = "Nutzer"
        verbose_name = "Nutzer"
        
    def __str__(self):
        return self.Name
 
    