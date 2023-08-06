# FileCache-jingle1267

Small high-performance file caching tool for python.

### Can do what?

You can set cache file easily, just focus on your business.

### How to use?

#### 1. import

```python
from FileCache import FileCache
```

#### 2. USE

```python
FileCache.easy_cache('test_cache_file.json', 'cache_key', test_hit_callback, test_miss_callback, a=1, b='c')
```

各个参数的含义：

```python
# 快速缓存便利工具
# file_name: 缓存文件名称
# cache_key：缓存字段名
# hit_callback：命中缓存需要执行的回调
# miss_callback：没有命中缓存需要执行的回调
# kwargs：回调需要传的参数
def easy_cache(file_name, cache_key, hit_callback, miss_callback, **kwargs)
```


#### 3. Config(Optional)

##### 3.1 Set cache folder path

```python
FileCache.CACHE_DIR = './tests'
```

##### 3.2 Set cache file sections

```python
FileCache.CACHE_FILE_SECTION_COUNT = 2
```

Better performance can be achieved by properly setting sections count.