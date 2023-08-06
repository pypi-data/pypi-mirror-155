from sklearn4x.core.BaseSerializer import BaseSerializer


class MultinomialNaiveBayesSerializer(BaseSerializer):
    def identifier(self):
        return 'nb_multinomial_serializer'

    def get_fields_to_be_serialized(self, model, version):
        fields = []
        self.add_field(fields, 'class_count_', model.class_count_)
        self.add_field(fields, 'class_log_prior_', model.class_log_prior_)
        self.add_field(fields, 'classes_', model.classes_)
        self.add_field(fields, 'feature_count_', model.feature_count_)
        self.add_field(fields, 'feature_log_prob_', model.feature_log_prob_)

        self.add_n_features(fields, model)
        self.add_feature_names(fields, model)

        return fields
