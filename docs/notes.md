# Caching

How do we look things up in the cache? Each instance of a task needs, in some sense, an ID. But really I think this ID should be derived from its type, its inputs, and its outputs. 

So a "render-pdf" task with input `[File('in.txt')]` and output `['out.pdf']` would have an ID like 'render-pdf-[in.txt]-[out.pdf]', at least in spirit. Maybe a json string would be useful: { type: 'render-pdf', inputs: ['in.txt'], outputs: ['out.pdf']}.

So each Node would need to be able to report its 'cache-id', i.e. the value that ends up in the Task's cache-id. 

Also each Node would need to be able to report a 'cache-value', i.e. some representation of its value which can be used to determine if its out of date. FOr files this could be a hash of file contents or a timestamp.

## Cache structure

The cache maps task cache-ids to a the relevant node values:

```
{ type: 'render-pdf', inputs: ['in.txt'], outputs: ['out.pdf']} =>  {input-values: [<in.txt timestamp>], output-values: [<out.pdf timestamp>]}
```

That is, for a given task plus its inputs and outputs, what were the cache-values of those nodes that last time it was built. Then when building we can fetch these cache-values. We actually run a task when:

1. The values aren't in the cache
2. Any cached input values are different from their state now -> an input has changed, forcing a rebuild
3. Any cached output value is different from their state now -> the output is not in the expected state (perhaps modified externally) and needs to be rebuilt.

