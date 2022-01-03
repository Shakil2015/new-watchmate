from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        exclude = ('watchlist',)
        #fields = "__all__"
class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True,read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only = True)
    #url = serializers.HyperlinkedIdentityField(view_name="testapp:stream_details")
    #watchlist =serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='movie_details')
    class Meta:
        model = StreamPlatform
        fields = "__all__"



    # def get_name_description(self,obj):
    #     return obj.name + " " + obj.description

    # def validate(self,data):
    #     if data['name']== data['description']:
    #         raise serializers.ValidationError('Name and description must be deffered')
    #     else:
    #         return data
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError('Name is too short')
    #     else:
    #         return value



# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, max_length=50)
#     description = serializers.CharField(required=True, max_length=100)
#     active = serializers.BooleanField( default=True)

#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)
#     def update(self,instance ,validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     def validate(self,data):
#         if data['name']== data['description']:
#             raise serializers.ValidationError('Name and description must be deffered')
#         else:
#             return data
#     def validate_name(self,value):
#         if len(value)<2:
#             raise serializers.ValidationError('Name is too short')
#         else:
#             return value