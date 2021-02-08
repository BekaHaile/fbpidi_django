from rest_framework import serializers
from collaborations.models import PollsQuestion, PollsResult, Choices
from accounts.api.serializers import UserSerializer
    

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = "__all__"
    

class PollsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollsResult
        fields  ="__all__"
    

class PollCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = PollsQuestion
        fields = ('user','title', 'title_am', 'description', 'description_am')
    
    def save(self, user):
        poll = PollsQuestion( user = user, title = self.validated_data['title'], title_am=self.validated_data['title_am'],
                            description=self.validated_data['description'], description_am=self.validated_data['description_am']
                        )
        poll.save()
        return poll


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many = True, read_only=True, required=False)
    pollsresult = PollsResultSerializer(many = True, read_only = True, required=False)
    
    class Meta:
        model = PollsQuestion
        fields = "__all__"

