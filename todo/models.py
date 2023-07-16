from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    



class User_info(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_name')
    assigned_distributor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_dependency')
    Proprietor_name = models.CharField(max_length=40)
    Mobile_Number = models.CharField(max_length=40)
    Email_ID = models.CharField(max_length=40)
    Address = models.CharField(max_length=40)
    role = models.CharField(max_length=40)
    verified= models.BooleanField(default=False)
    def __str__(self):
        if self.verified == False:
            return self.user.username + " {" + self.Proprietor_name + "} : [Not verified yet]" 
        else:
            return self.user.username + " {" + self.Proprietor_name + "}"

class Order_info(models.Model):
    pt = (
        ('Spl_Urad_100g', 'Spl-Urad(100g)'), ('Spl_Urad_200g', 'Spl-Urad(200g)'), ('Spl_Urad_1kg', 'Spl-Urad(1kg)'),
        ('Plain_Urad_100g', 'Plain-Urad(100g)'), ('Plain_Urad_200g', 'Plain-Urad(200g)'), ('Plain_Urad_1kg', 'Plain-Urad(1kg)'),
        
        ('Urad_Moong_100g', 'Urad-Moong(100g)'), ('Urad_Moong_200g', 'Urad-Moong(200g)'), ('Urad_Moong_1kg', 'Urad-Moong(1kg)'),
        ('Garlic_Green_Chilli_100g', 'Garlic-Green-Chilli(100g)'), ('Garlic_Green_Chilli_200g', 'Garlic-Green-Chilli(200g)'), ('Garlic_Green_Chilli_1kg', 'Garlic-Green-Chilli(1kg)'),
        
        ('Spl_Green_Chilli_100g', 'Spl-Green-Chilli(100g)'), ('Spl_Green_Chilli_200g', 'Spl-Green-Chilli(200g)'), ('Spl_Green_Chilli_1kg', 'Spl-Green-Chilli(1kg)'),
        ('Spl_Garlic_100g', 'Spl-Garlic(100g)'), ('Spl_Garlic_200g', 'Spl-Garlic(200g)'), ('Spl_Garlic_1kg', 'Spl-Garlic(1kg)'),

        ('Red_Chilli_100g', 'Red-Chilli(100g)'), ('Red_Chilli_200g', 'Red-Chilli(200g)'), ('Red_Chilli_1kg', 'Red-Chilli(1kg)'),
        ('Jeera_100g)', 'Jeera(100g)'), ('Jeera_200g', 'Jeera(200g)'), ('Jeera_1kg', 'Jeera(1kg)'),

        ('Spl_Panjabi_100g', 'Spl-Panjabi(100g)'), ('Spl_Panjabi_200g', 'Spl-Panjabi(200g)'), ('Spl_Panjabi_1kg', 'Spl-Panjabi(1kg)'),
        ('Chana_Mix_100g', 'Chana-Mix(100g)'), ('Chana_Mix_200g', 'Chana-Mix(200g)'), ('Chana_Mix_1kg', 'Chana-Mix(1kg)'),

        ('Whole_Moong_100g', 'Whole-Moong(100g)'), ('Whole_Moong_200g', 'Whole-Moong(200g)'), ('Whole_Moong_1kg', 'Whole-Moong(1kg)'),
        ('Jain_100g', 'Jain(100g)'), ('Jain_200g', 'Jain(200g)'), ('Jain_1kg', 'Jain(1kg)'),
        
        ('Coin_1kg', 'Coin(1kg)'),

        )
    
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_name_order_info')
    papad_type = models.CharField(max_length=40, choices=pt)
    quantity = models.PositiveIntegerField()
    date_time = models.DateTimeField(default=datetime.now, blank=True)    
    comment = models.CharField(max_length=40)
    acknowledgement = models.BooleanField(default=False)
    order_placed = models.BooleanField(default=False)
    responsible_firm_of_this_order = models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_responsible_firm')

    def __str__(self):
        if self.acknowledgement == False:
            return self.user.username + " ("  +self.papad_type +  " ) : [Order Not Acknowledgement]" 
        elif self.order_placed == False:
            return  self.user.username + " ("  +self.papad_type +  " ) : [Order Not placed]" 
        else:
            return  self.user.username + " ("  +self.papad_type +  " )"


class product_inventry_info(models.Model):
    product_name = models.CharField(max_length=40)
    product_qty =  models.PositiveIntegerField()
    ideal_qty =  models.PositiveIntegerField()
    comment =  models.CharField(default="comment", max_length=40)
    def __str__(self):
        return self.product_name + " {" + str(self.product_qty) + "}"

class raw_inventry_info(models.Model):
    product_name = models.CharField(max_length=40)
    product_qty =  models.PositiveIntegerField()
    ideal_qty =  models.PositiveIntegerField()
    comment =  models.CharField(default="comment", max_length=40)
    def __str__(self):
        return self.product_name + " {" + str(self.product_qty) + "}"

