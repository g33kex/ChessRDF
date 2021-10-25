Example SPARQL requests on `academic.ttl` database

## 1. Quel est le nom de l’enseignant(e) ayant offert le cours de sigle  ”INF8410” à l’étudiant nommé ”Jesse” et à quelle session ?

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
## 2. Quel  sont  les  noms  des  étudiants  ayant  suivis  le  cours  intitulé  ”Champs électromagnétiques” avec l’étudiante nommée ”Violet”? (Violet peut elle-même se retrouver dans cette liste).  

```sparql
SELECT DISTINCT ?name
WHERE {
  ?student exemple:name ?name ;
  exemple:takesClass ?class .
  {
  SELECT ?class
  WHERE {
    ?class exemple:class/exemple:titleClass "Champs électromagnétiques" ;
    ^exemple:takesClass/exemple:name "Violet" .
    }
  }
}

```
