from wrap_engine import id_generator


class Object_manager():
    def __init__(self):
        self._objects = {}  # id:obj
        self._id_generator = id_generator.Usual_id_generator()

    def _get_obj_id(self, obj):
        for id, val in self._objects.items():
            if obj is val:
                return id
        return None

    def add_object(self, obj):
        # get existent id
        if obj in self._objects.values():
            return self._get_obj_id(obj)

        new_id = self._id_generator.get_id()
        self._objects[new_id] = obj
        return new_id

    def remove_by_id(self, id):
        if id in self._objects:
            obj = self._objects[id]
            del self._objects[id]
            return obj
        return None

    def get_obj_id(self, obj):
        return self._get_obj_id(obj)

    def get_obj_by_id(self, id):
        if id in self._objects.keys():
            return self._objects[id]
        else:
            return None

    #not existent ids just skipped
    def get_obj_list_by_id_list(self, id_list):
        res = []
        for id in id_list:
            if id in self._objects.keys():
                res.append(self._objects[id])

        return res

    #not existent objects just skipped
    def get_id_list_by_obj_list(self, obj_list):
        res = []
        for id, val in self._objects.items():
            if val in obj_list:
                res.append(id)

        return res
