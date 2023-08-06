# property_accessor
Python property accessor module util


### Installation:
```shell
> poetry add property-accessor
```

### Usage

```python
from property_accessor import PropertyAccessor
from dataclasses import dataclass, field


@dataclass
class Category:
    code: str

@dataclass
class Product:

    name: str
    sku: str
    price: float
    categories: list[Category] = field(default=list)


accessor = PropertyAccessor(None)

accessor.set('sku', 't-shirt-01')
accessor.set('name', 't-shirt basic black')
accessor.set('price', 39.9)
accessor.set('categories[0].code', 't-shits')

print(accessor.get('name')) # t-shirt basic black
print(accessor.get('categories[0].code')) # t-shirt


print(accessor.data) # AnonymousObject(sku='t-shirt-01', name='t-shirt basic black', price=39.9, categories=[AnonymousObject(code="t-shirts")])
print(accessor.data.cast(Product)) # Product(sku='t-shirt-01', name='t-shirt basic black', price=39.9, categories=[Category(code="t-shirts")])
```