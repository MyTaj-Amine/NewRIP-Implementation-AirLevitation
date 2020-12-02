class CommandBuilder(object):
    @staticmethod
    def get_model_workspace(model):
        return "mws = get_param('" + model + "', 'modelworkspace');"

    @staticmethod
    def to_model_workspace(name, value):
        return "mws.assignin('" + name + "', " + str(value) + "); \n"
