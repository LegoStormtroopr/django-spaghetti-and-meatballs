from django.db import models

class PoliceOfficer(models.Model):
    """
    An officer of the NYPD
    """
    badge_number = models.IntegerField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    rank = models.CharField(max_length=200)
    
    arrests = models.ManyToManyField("Arrest",related_name="arresting_officers")

class Precinct(PoliceStation):
    number = models.IntegerField(max_length=10)
    burrough = models.CharField(max_length=20)
    captain = models.OneToOneField(PoliceOfficer)
    officers = models.ForeignKey("PoliceOfficer",related_name="precinct")
    
    class Meta:
        unique_together = ("burrough","number")
    def natural_key(self):
        return (self.burrough,self.number)

class Division(PoliceStation):
    name = models.CharField(max_length=200)
    officers = models.ForeignKey("PoliceOfficer",related_name="division")

class Arrest(models.Model):
    alleged_crime = models.CharField(max_length=20)
    perp = models.ForeignKey("Perpetrator")
    arrest_date = models.DateField()
    processing_date = models.DateField()

class Perpetrator(models.Model):
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birth_date = models.DateField()
