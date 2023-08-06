# jonschema

## Presentation

**jonschema** is a dependency allowing you to validate multiple data types in a precise and fast way.

## Installation

```console
pip install jonschema
```
## Use

### Number

```python
import jonschema
value = 12
# init validation
# res = jonschema.Number().required().default(10).label('entier1').validate(value)
# min
# res = jonschema.Number().min(5).required().label('entier1').validate(value)
# max
# res = jonschema.Number().min(5).max(50).required().label('entier1').applyApp(
#     rule = lambda value: value > 40,
# ).applyMapping(lambda value: value * 10).defaultError({
#     'fr': "votre element est invalide",
#     'en': "your element is invalid",
# }).validate(value)
# less
# res = jonschema.Number().less(5).required().label('entier1').validate(value)
# greater
# res = jonschema.Number().less(5).greater(50).required().label('entier1').validate(value)
# negative
# res = jonschema.Number().negative().label('entier1').validate(value)
# positive
# res = jonschema.Number().positive().min(11).label('entier1').validate(value)
# signed
# res = jonschema.Number().signed().label('entier1').validate(value)
# integer
# res = jonschema.Number().integer().label('entier1').validate(value)
# decimal
# res = jonschema.Number().decimal().label('entier1').validate(value)
# multiple
# res = jonschema.Number().multiple(3).label('entier1').validate(value)
# port
res = jonschema.Number().TCPPort().label('entier1').validate(value)

print("> res:: ", res)
print("> res['error']:: ", res['error'])
return res
```

#### .min(min_value)

```py
import jonschema
schema = jonschema.Number()
const schema = new jonschema.Number().min(3)
```

##### Arguments

| Property | Description | Type |
| :-------- | :---------- | :--- |
| **min_value** | the number to be validated must be less than or equal to min_value | **Number** |

## Useful links

* [Git](/ "https://ntouba98@bitbucket.org/ntouba98/jonpy.git")
* [Nodejs dependency](/ "https://pypi.org/project/jonschema/")