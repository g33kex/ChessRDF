Example SPARQL requests on `academic.ttl` database

## 1. Quel est le nom de l’enseignant(e) ayant offert le cours de sigle  ”INF8410” à l’étudiant nommé ”Jesse” et à quelle session ?

```sparql
SELECT DISTINCT ?name ?session
WHERE {
  ?teacher exemple:name ?name;
  exemple:givesClass ?class .
  ?class exemple:class/exemple:sigleClass "INF8410".
  ?class  ^exemple:takesClass/exemple:name "Jesse";
  exemple:session ?session.
}
```
## 2. Quel  sont  les  noms  des  étudiants  ayant  suivis  le  cours  intitulé  ”Champs électromagnétiques” avec l’étudiante nommée ”Violet”? (Violet peut elle-même se retrouver dans cette liste).  

```sparql
SELECT DISTINCT ?name
WHERE {
  ?student exemple:name ?name ;
  exemple:takesClass ?class .
  ?class exemple:class/exemple:titleClass "Champs électromagnétiques" ;
  ^exemple:takesClass/exemple:name "Violet" .
}

```

## 3. Quel est l’enseignant(e) ayant offert le plus de cours au total sur toutes les sessions et combien en a-t-il(elle) offert(e) ?

```sparql
SELECT ?name (MAX(?tot) AS ?max)
WHERE {
{
  SELECT ?name (COUNT(?class) AS ?tot)
  WHERE {
    ?teacher exemple:name ?name;
    exemple:givesClass ?class .
  }
  GROUP BY ?teacher
}
}
```

## 4.  L’étudiant nommé ”Leonard” a-t-il  suivi  les  11  cours  offerts  au  moins  une  fois chacun ? 

ASK
WHERE {
  ?student exemple:name "Leonard" ;
  exemple:takesClass/exemple:class ?class .

}
HAVING(COUNT(distinct ?class) = 11)

## 5. Quelle est la moyenne du nombre de crédits suivis par les étudiants pour chaque session ?

SELECT (AVG(?sum) AS ?avg) 
WHERE {
{
  SELECT ?session (SUM(?nbcredit) AS ?sum) 
  WHERE {
    ?etudiant exemple:takesClass ?class .
    ?class exemple:class/exemple:numberCredits ?nbcredit .
    ?class exemple:session ?session .
  }
  GROUP BY ?etudiant
}
}
GROUP BY ?session
