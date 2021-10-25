Example SPARQL requests on `academic.ttl` database

## 1 Quel est le nom de l’enseignant(e) ayant offert le cours de sigle  ”INF8410” à l’étudiant nommé ”Jesse” et à quelle session ?

```sparql
SELECT DISTINCT ?name ?session
WHERE {
  ?teacher exemple:name ?name;
  exemple:givesClass ?class .
  {
    SELECT ?class ?session
    WHERE {
    ?class exemple:class/exemple:sigleClass "INF8410".
    ?class  ^exemple:takesClass/exemple:name "Jesse";
    exemple:session ?session.
    }
  }
}
```
