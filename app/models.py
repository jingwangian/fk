from . import db


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    obss = db.relationship('Observation', backref='survey', lazy='dynamic')

    # def __repr__(self):
    #     return '<Survey {}>'.format(self.name)

    def get_all_obs(self):
        return [ob for ob in self.obss.all()]

    def to_json(self):
        return {"id": self.id, "name": self.name}

    def mean(self):
        total_value = sum([ob.value * ob.frequency for ob in self.get_all_obs()])

        print(f'mean total_value:{total_value}/count:{self.count()}')

        try:
            mean = total_value / self.count()
        except ZeroDivisionError:
            return 0

        return round(mean, 2)

    def count(self):
        count_value = sum([ob.frequency for ob in self.get_all_obs()])

        return round(count_value, 2)

    def median(self):
        count = self.count()

        if count == 0:
            return 0

        ob_value_list = []
        for ob in self.get_all_obs():
            ob_value_list.extend([ob.value] * ob.frequency)

        ob_value_list.sort()

        # print('mean sorted ob_value_list:', ob_value_list)

        list_len = len(ob_value_list)

        if list_len % 2 == 0:
            median = (ob_value_list[int(list_len / 2) - 1] + ob_value_list[int(list_len / 2)]) / 2
        else:
            median = ob_value_list[int(list_len / 2)]

        return round(median, 2)

    def mode(self):
        obs = self.get_all_obs()

        if len(obs) == 0:
            return [0]

        frequency_list = list(set([ob.frequency for ob in obs]))

        # print('In mode frequency_list:', frequency_list)
        mode_key = frequency_list[-1]

        return [ob.value for ob in obs if ob.frequency == mode_key]


class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    value = db.Column(db.Float)
    frequency = db.Column(db.Integer)

    def __repr__(self):
        return f'<Observation: id=[{self.id}], \
            survey_id=[{self.survey_id}], value=[{self.value}], frequency=[{self.frequency}]>'

    def to_json(self):
        return {"id": self.id,
                "survey_id": self.survey_id,
                "value": self.value,
                "frequency": self.frequency}
