from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers


class FsmViewSetMixin(APIView):
    fsm_fields = []

    @classmethod
    def get_fsm_fields(cls):
        return cls.fsm_fields

    @classmethod
    def get_all_transitions(cls, field_name):
        model = cls.queryset.model
        field = getattr(model, field_name).field
        transitions = field.get_all_transitions(model)
        filter_transitions = cls.filter_transitions(field_name, transitions)
        return filter_transitions

    @classmethod
    def filter_transitions(cls, field_name, transitions):
        """
            @classmethod
            def status_transitions(cls):
                return ['pending', 'complete']

        """
        transitions_state_method_name = f"{field_name}_transitions"
        transitions_state_method = getattr(cls, transitions_state_method_name, None)
        if transitions_state_method and callable(transitions_state_method):
            transitions_name = transitions_state_method()
            transitions = filter(lambda x: x.name in transitions_name, transitions)
        return transitions

    @classmethod
    def get_extra_actions(cls):
        """
        Get the methods that are marked as an extra ViewSet `@action`.

        """
        actions = super().get_extra_actions()
        for field in cls.get_fsm_fields():
            class PostSerializer(serializers.ModelSerializer):
                def get_field_names(self, declared_fields, info):
                    fields = super().get_field_names(declared_fields, info)
                    fields.append(field)
                    return fields

                class Meta:
                    model = cls.queryset.model
                    fields = []

            @action(methods=['post'], detail=True,
                    url_path=f"{field}",
                    url_name=f"{field}-transition", name=f"{field}".title(),
                    serializer_class=cls.get_fsm_serializer_class(field))
            def inner_func(self, request, args, *kwargs):
                instance = self.get_object()
                serializer_class = PostSerializer
                serializer = serializer_class(data=request.data, instance=instance,
                                              context={"request": request, "field": field, "action": self.action})
                serializer.is_valid(raise_exception=True)
                state = serializer.validated_data[field]
                # Calling transition method
                getattr(instance, state.lower())()
                instance.save()
                data = self.get_fsm_serializer_data(serializer, field)
                return Response(data)

            inner_func.__name__ = field
            inner_func.mapping = {'post': field}
            setattr(cls, field, inner_func)
            actions.append(inner_func)

        return actions

    @classmethod
    def get_fsm_serializer_class(cls, field):
        """
        ex: field = status
        first trying to find {field}_serializer_class
            serializer_class = status_serializer_class

         still not exist above then using default serializer_class of view
        """
        return getattr(cls, f"{field}_serializer_class", cls.serializer_class)

    def get_fsm_serializer_data(self, serializer, field):
        response_method_name = f"{field}_response"
        response_method = getattr(self, response_method_name, None)
        if response_method and callable(response_method):
            return response_method(serializer)
        return serializer.data
