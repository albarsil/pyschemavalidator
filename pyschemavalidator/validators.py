from .parameters import BaseParameter

class Response(object):
    BAD_PARAM_TYPE = "Input type error for parameter: {}; Expected: {} but got {}"
    BAD_PARAM_INNERTYPE = "Input inner type error for parameter: {}; Expected: {} but got {}"
    BAD_PARAM_BONDUARY = "Failed to check constrains for parameter: {}; Expect values between {} and {} but got: {}"
    FAILED_CONSTRAINS_PARAM = "Failed to check constrains for parameter: {}. Expected: [{}] but got: {}"
    MISSING_REQUIRED_PARAM = "Missing required parameter in body: [{}]"
    UNKNOWN_PARAM = "The parameter {} was not declared as part of the validations"
    MISSING_VALIDATION = "Not validated parameter declared as part of the validations: [{}]"
    MISSING_JSON_BODY = "Missing JSON object in body"


class UniversalValidator(object):

    def __init__(self):
        self._validations = {}

    def add(self, key: str, keytype: str, isrequired: bool, innertype=None, maxmin: tuple=None, constrain: tuple=None):
        """
            Add a new parameter with the specified key and restrictions

            inputs:
                key: The parameter name
                keytype: The parameter type
                isrequired: True if the parameter is required else False
                innertype: If keytype is list, tuple or set, then you can use this argument to define the inner type of this collection
                maxmin: If one of keytype or innertype are int or float then you can use this argument to define a bonduary to it. Like (0,10)
                constrain: If one of keytype or innertype are str or boolean then you can use this argument to define a constrain list to their values

            outputs:
                void
        """

        if keytype in (list, tuple, set):
            if innertype == None:
                raise ValueError("If keytype is subtype of list, then you should set the innertype value")
            elif (maxmin != None) & (innertype not in (int, float)):
                raise ValueError("Max and min value should be set just if innertype is numeric")
            elif (constrain != None) & (innertype not in (str, int, bool)):
                raise ValueError("Constrain value should be set just if innertype is str, int or bool")
        else:
            if (maxmin != None) & (keytype not in (int, float)):
                raise ValueError("Max and min value should be set just if keytype is numeric")

            if (constrain != None) & (keytype not in (str, int, bool)):
                raise ValueError("Constrain value should be set just if keytype is str, int or bool")

        self._validations[key] = Parameter(
            key = key,
            keytype = keytype,
            innertype = innertype,
            isrequired = isrequired,
            max = maxmin[1] if maxmin != None else None,
            min = maxmin[0] if maxmin != None else None,
            constrain = constrain
        )

    def validate(self, **kwargs) -> tuple:
        """
            Validate the arguments received by param with those ones defined on add

            inputs:
                - kwargs: A dictionary with key and value, which should match with the ones defined on add
            
            outputs:
                It returns a tuple with the status code of the request and the message
        """

        # Check if some of the parameters are missing
        notfounds = [x for x in self._validations.keys() if x not in kwargs.keys()]
        requireds = [k for k,v in kwargs.items() if (self._validations[k].isrequired == True) & (v == None)] # Check if some of the required parameters are missing
        
        if len(notfounds) > 0:
            raise ValueError(Response.MISSING_VALIDATION.format(",".join(notfounds)))
            
        if len(requireds) > 0:
            return 400, Response.MISSING_REQUIRED_PARAM.format(",".join(requireds))
        
        # Iterates over the input params and their values
        for key, value in kwargs.items():
            if key not in self._validations:
                return 500, ValueError(Response.UNKNOWN_PARAM.format(key))

            # Compare if the key is required or not
            if ((self._validations[key].isrequired == False) & (value == None)):
                continue
            
            # Compare the key types
            if isinstance(value, self._validations[key].keytype) == False:
                return 400, Response.BAD_PARAM_TYPE.format(key, self._validations[key].keytype, str(type(value)))

            # Compare the key bounduaries if was set
            if (self._validations[key].min != None and self._validations[key].max != None) & ((self._validations[key].keytype == float) | (self._validations[key].keytype == int)):
                if ((value > self._validations[key].max) | (value < self._validations[key].min)):
                    return 400, Response.BAD_PARAM_BONDUARY.format(key, self._validations[key].min, self._validations[key].max, str(value))
            
            # Compare the key list elements
            if ((self._validations[key].keytype == list) | (self._validations[key].keytype == set) | (self._validations[key].keytype == tuple)):

                # Compare the all the list elements have the type set
                elements = [x for x in value if type(x) != self._validations[key].innertype]
                if len(elements) > 1:
                    return 400, Response.BAD_PARAM_INNERTYPE.format(key, self._validations[key].innertype, ",".join([str(x) for x in elements]))

                # Compare the list constrains if set
                if self._validations[key].constrain != None:
                    elements = [x for x in value if x not in self._validations[key].constrain]
                    if len(elements) > 0:
                        return 400, Response.FAILED_CONSTRAINS_PARAM.format(key, ",".join(self._validations[key].constrain), ",".join([str(x) for x in elements]))

                # Compare the list inner bonduaries if set
                if ((self._validations[key].min != None) & (self._validations[key].max != None)):
                    elements = [x for x in value if ((x > self._validations[key].max) | (x < self._validations[key].min))]
                    if len(elements) > 0:
                        return 400, Response.BAD_PARAM_BONDUARY.format(key, self._validations[key].min, self._validations[key].max, ",".join([str(x) for x in elements]))

        return 200, None