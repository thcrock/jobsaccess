from django.db import models


class PhaseAchieved(models.Model):
    description = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        db_table = "phases_achieved"


class ReachableCoordinates(models.Model):
    latitude_start = models.CharField(max_length=12)
    longitude_start = models.CharField(max_length=12)
    depart_time = models.DateTimeField()
    transit_time = models.IntegerField()
    phase_achieved = models.ForeignKey(PhaseAchieved)
    latitude_reachable = models.CharField(max_length=7)
    longitude_reachable = models.CharField(max_length=8)

    class Meta:
        db_table = "reachable_coordinates"


class CensusBlock(models.Model):
    census_block = models.CharField(max_length=15)
    workforce_segment = models.CharField(max_length=6)
    C000 = models.IntegerField(null=True)
    CA01 = models.IntegerField(null=True)
    CA02 = models.IntegerField(null=True)
    CA03 = models.IntegerField(null=True)
    CE01 = models.IntegerField(null=True)
    CE02 = models.IntegerField(null=True)
    CE03 = models.IntegerField(null=True)
    CNS01 = models.IntegerField(null=True)
    CNS02 = models.IntegerField(null=True)
    CNS03 = models.IntegerField(null=True)
    CNS04 = models.IntegerField(null=True)
    CNS05 = models.IntegerField(null=True)
    CNS06 = models.IntegerField(null=True)
    CNS07 = models.IntegerField(null=True)
    CNS08 = models.IntegerField(null=True)
    CNS09 = models.IntegerField(null=True)
    CNS10 = models.IntegerField(null=True)
    CNS11 = models.IntegerField(null=True)
    CNS12 = models.IntegerField(null=True)
    CNS13 = models.IntegerField(null=True)
    CNS14 = models.IntegerField(null=True)
    CNS15 = models.IntegerField(null=True)
    CNS16 = models.IntegerField(null=True)
    CNS17 = models.IntegerField(null=True)
    CNS18 = models.IntegerField(null=True)
    CNS19 = models.IntegerField(null=True)
    CNS20 = models.IntegerField(null=True)
    CR01 = models.IntegerField(null=True)
    CR02 = models.IntegerField(null=True)
    CR03 = models.IntegerField(null=True)
    CR04 = models.IntegerField(null=True)
    CR05 = models.IntegerField(null=True)
    CR07 = models.IntegerField(null=True)
    CT01 = models.IntegerField(null=True)
    CT02 = models.IntegerField(null=True)
    CD01 = models.IntegerField(null=True)
    CD02 = models.IntegerField(null=True)
    CD03 = models.IntegerField(null=True)
    CD04 = models.IntegerField(null=True)
    CS01 = models.IntegerField(null=True)
    CS02 = models.IntegerField(null=True)
    CFA01 = models.IntegerField(null=True)
    CFA02 = models.IntegerField(null=True)
    CFA03 = models.IntegerField(null=True)
    CFA04 = models.IntegerField(null=True)
    CFA05 = models.IntegerField(null=True)
    CFS01 = models.IntegerField(null=True)
    CFS02 = models.IntegerField(null=True)
    CFS03 = models.IntegerField(null=True)
    CFS04 = models.IntegerField(null=True)
    CFS05 = models.IntegerField(null=True)

    class Meta:
        db_table = "census_blocks"


class BlockLocations(models.Model):
    latitude = models.CharField(max_length=7)
    longitude = models.CharField(max_length=8)
    census_block = models.ForeignKey(CensusBlock)

    class Meta:
        db_table = "block_locations"
