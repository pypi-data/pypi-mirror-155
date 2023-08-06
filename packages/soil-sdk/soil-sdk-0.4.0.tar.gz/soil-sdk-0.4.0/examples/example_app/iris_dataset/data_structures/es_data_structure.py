""" A generic datastructure to index stuff to Elastic Search """
from soil.data_structures.data_structure import DataStructure
from soil.storage.elasticsearch import Elasticsearch
import soil

#########
# UTILS #
#########

MATCH_ALL = {"match_all": {}}
QUERY_ALL = {"query": MATCH_ALL}


def iris_to_es_query(filters):
    """
    Build elastic search query
    """
    must = []
    if filters is None:
        soil.logger.warning("NONE FILTERS")
    for f in filters:
        if f is None:
            return MATCH_ALL
        if "fn" not in f:
            soil.logger.warning("Query function not found!")
            return MATCH_ALL
        if f["fn"] == "list":
            must.append({"terms": {f["variable"]: f["value"]}})
        elif f["fn"] == "list-deactivated-default":
            if len(f["value"]) > 0:
                must.append({"terms": {f["variable"]: f["value"]}})
        elif f["fn"] == "equal":
            must.append({"term": {f["variable"]: f["value"]}})
        elif f["fn"] == "range":
            must.append({"range": {f["variable"]: f["value"]}})
        else:
            soil.logger.warning("Query function not found!")

    if not must:
        return {"bool": {"must": must}}
    return MATCH_ALL


def get_agg(variable):
    """
    Build an aggregation
    """
    if variable["type"] in {"terms", "avg"}:
        return {variable["name"]: {variable["type"]: {"field": variable["variable"]}}}
    return None


def iris_to_es_aggs(aggregation):
    """
    Build aggregations
    """
    if len(aggregation) == 1:
        variable = aggregation[0]
        return get_agg(variable)
    aggs = {}
    for variable in aggregation:
        aggs[variable["name"]] = get_agg(variable)[variable["name"]]

    return aggs


def get_barchart_count(hits, label="label"):
    """
    Get the barchart for counting elements in buckets
    """
    serie = []
    for d in hits["group_by_type"]["buckets"]:
        serie.append({"x": d["key"], "y": d["doc_count"]})

    if len(serie) == 0:
        return "empty"

    data = [{"serie": label, "data": serie}]
    return data


def get_barchart_sizes(hits):
    """
    Get the barchart with the measurements of the plants
    """
    data = [
        {
            "serie": "Petal",
            "data": [
                {"x": "Width", "y": hits["petal_width"]["value"]},
                {"x": "Length", "y": hits["petal_length"]["value"]},
            ],
        },
        {
            "serie": "Sepal",
            "data": [
                {"x": "Width", "y": hits["sepal_width"]["value"]},
                {"x": "Length", "y": hits["sepal_width"]["value"]},
            ],
        },
    ]
    return data


def get_hits_count(hits):
    """
    Count how many hits we have
    """
    # THIS CAN BE DONE WAY MORE EFFICIENTLY!
    return len(hits)


fns = {
    "get_barchart_sizes": get_barchart_sizes,
    "get_barchart_count": get_barchart_count,
    "get_hits_count": get_hits_count
}


##################
# DATA STRUCTURE #
##################


class ESDataStructure(DataStructure):
    # pylint:disable=attribute-defined-outside-init, access-member-before-definition
    """A generic datastructure to index stuff to Elastic Search"""

    def serialize(self):
        """
        Serializes the data and stores them using Elasticsearch.
        The data must be json serializable.
        """
        elasticsearch = Elasticsearch(index=self.metadata["index"])
        if self.metadata.get("rewrite", False):
            elasticsearch.delete_index()
        elasticsearch.create_index(schema=self.metadata.get("schema", None))
        elasticsearch.bulk(self.data)
        return elasticsearch

    @classmethod
    # The argument order is given by DataStructure!
    def deserialize(cls, es_storage, metadata):
        """
        Deserializes the data obtaining them from ObjectStorage.
        """
        if es_storage is not None and isinstance(es_storage, Elasticsearch):
            # If a datastructure comes from a database, it is prefered not to return data
            # because we do not know its size and we might want to make queries.
            # In modules, data might be accesed using get_data() or the iterator (list(ESDataStructure)).
            return cls(None, metadata, storage=es_storage)
        raise NotImplementedError("ESDataStructure without ES not implemented")

    # If we want to acces data through an interator
    def __iter__(self):
        if self.data is None:
            result = self.storage.search(
                {"query": {"match_all": {}}}, auto_scroll=True
            )  # autoscroll True the data is returned in blocks of 10000 entries
            self.data = result[0]
            self.iter = iter(self.data)
        return self

    def __next__(self):
        return next(self.iter)

    def get_data(
        self,
        query=None,
        source=None,
        aggregation=None,
        fn=None,
        fn_args=None,
        lang="ca",
    ):
        """Serialize the data for JSON the data"""

        # Return empty if there is no query
        if query is None:
            return []

        # Extract the typof query
        query_type = query["type"]

        # If the query type is iris
        if query_type == "iris":
            filters = query["filters"]
            return self.get_data_iris(
                query_type,
                filters,
                aggregation=aggregation,
                fn=fn,
                fn_args=fn_args,
                lang=lang,
                source=source,
            )

        # else
        soil.logger.warning("Query type {query_type} not implemented.")
        return []

    def get_data_iris(
        self,
        qtype,
        filters,
        aggregation=None,
        source=None,
        fn=None,
        fn_args=None,
        lang="ca",
    ):
        """
        Build and return query to IRIS front end
        """

        # Build ES query
        question = {}

        if qtype == "ES":
            question["query"] = filters

        elif qtype == "iris":
            question["query"] = iris_to_es_query(filters)

        if aggregation is not None:
            question["aggs"] = iris_to_es_aggs(aggregation)

        if source is not None:
            question["_source"] = source

        # Call to ES
        if aggregation is not None:
            try:
                question["size"] = 0
                response = self.storage.search(question, auto_scroll=False)[
                    "aggregations"
                ]
            except KeyError as e:
                soil.logger.error("on no! %s", e)
        else:
            try:
                response = list(self.storage.search(question)[0])
            except KeyError as e:
                soil.logger.error("on no! %s", e)

        # Apply processing function if so
        soil.logger.info(lang)
        if fn is not None:
            if fn_args is None:
                fn_args = {}
            if fn in fns:
                response = fns[fn](response, **fn_args)
        return response
