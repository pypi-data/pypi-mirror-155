
import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';
export default [
{
  path: '/',
  component: ComponentCreator('/','deb'),
  exact: true,
},
{
  path: '/__docusaurus/debug',
  component: ComponentCreator('/__docusaurus/debug','3d6'),
  exact: true,
},
{
  path: '/__docusaurus/debug/config',
  component: ComponentCreator('/__docusaurus/debug/config','914'),
  exact: true,
},
{
  path: '/__docusaurus/debug/content',
  component: ComponentCreator('/__docusaurus/debug/content','c28'),
  exact: true,
},
{
  path: '/__docusaurus/debug/globalData',
  component: ComponentCreator('/__docusaurus/debug/globalData','3cf'),
  exact: true,
},
{
  path: '/__docusaurus/debug/metadata',
  component: ComponentCreator('/__docusaurus/debug/metadata','31b'),
  exact: true,
},
{
  path: '/__docusaurus/debug/registry',
  component: ComponentCreator('/__docusaurus/debug/registry','0da'),
  exact: true,
},
{
  path: '/__docusaurus/debug/routes',
  component: ComponentCreator('/__docusaurus/debug/routes','244'),
  exact: true,
},
{
  path: '/blog',
  component: ComponentCreator('/blog','4c4'),
  exact: true,
},
{
  path: '/blog/2016/03/11/blog-post',
  component: ComponentCreator('/blog/2016/03/11/blog-post','e97'),
  exact: true,
},
{
  path: '/blog/2017/04/10/blog-post-two',
  component: ComponentCreator('/blog/2017/04/10/blog-post-two','c24'),
  exact: true,
},
{
  path: '/blog/2017/09/25/testing-rss',
  component: ComponentCreator('/blog/2017/09/25/testing-rss','0d7'),
  exact: true,
},
{
  path: '/blog/2017/09/26/adding-rss',
  component: ComponentCreator('/blog/2017/09/26/adding-rss','c6e'),
  exact: true,
},
{
  path: '/blog/2017/10/24/new-version-1.0.0',
  component: ComponentCreator('/blog/2017/10/24/new-version-1.0.0','99f'),
  exact: true,
},
{
  path: '/docs',
  component: ComponentCreator('/docs','5fb'),
  
  routes: [
{
  path: '/docs/sdk-reference/soil/alerts/alerts',
  component: ComponentCreator('/docs/sdk-reference/soil/alerts/alerts','597'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/alias',
  component: ComponentCreator('/docs/sdk-reference/soil/alias','2cc'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/api',
  component: ComponentCreator('/docs/sdk-reference/soil/api','890'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/configuration',
  component: ComponentCreator('/docs/sdk-reference/soil/configuration','d6c'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/connectors/elastic_search',
  component: ComponentCreator('/docs/sdk-reference/soil/connectors/elastic_search','6ef'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/data',
  component: ComponentCreator('/docs/sdk-reference/soil/data','b69'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/data_structure',
  component: ComponentCreator('/docs/sdk-reference/soil/data_structure','557'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/decorator',
  component: ComponentCreator('/docs/sdk-reference/soil/decorator','80b'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/dictionary',
  component: ComponentCreator('/docs/sdk-reference/soil/dictionary','adc'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/finder',
  component: ComponentCreator('/docs/sdk-reference/soil/finder','025'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/modulify',
  component: ComponentCreator('/docs/sdk-reference/soil/modulify','9ad'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/pipeline',
  component: ComponentCreator('/docs/sdk-reference/soil/pipeline','986'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/storage/base_storage',
  component: ComponentCreator('/docs/sdk-reference/soil/storage/base_storage','bbe'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/storage/compound_storage',
  component: ComponentCreator('/docs/sdk-reference/soil/storage/compound_storage','6d5'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/storage/elasticsearch',
  component: ComponentCreator('/docs/sdk-reference/soil/storage/elasticsearch','660'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/storage/object_storage',
  component: ComponentCreator('/docs/sdk-reference/soil/storage/object_storage','999'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/task',
  component: ComponentCreator('/docs/sdk-reference/soil/task','b03'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/types',
  component: ComponentCreator('/docs/sdk-reference/soil/types','5bf'),
  exact: true,
},
{
  path: '/docs/sdk-reference/soil/utils',
  component: ComponentCreator('/docs/sdk-reference/soil/utils','55a'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/data_structure',
  component: ComponentCreator('/docs/soil-library/data_structures/data_structure','b5c'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/frequent_itemsets',
  component: ComponentCreator('/docs/soil-library/data_structures/frequent_itemsets','5cb'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/hypergraph',
  component: ComponentCreator('/docs/soil-library/data_structures/hypergraph','3a4'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/NBClusters',
  component: ComponentCreator('/docs/soil-library/data_structures/NBClusters','254'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/predefined/dict',
  component: ComponentCreator('/docs/soil-library/data_structures/predefined/dict','f8a'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/predefined/list',
  component: ComponentCreator('/docs/soil-library/data_structures/predefined/list','c8c'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/predefined/ndarray',
  component: ComponentCreator('/docs/soil-library/data_structures/predefined/ndarray','789'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/predefined/object_ds',
  component: ComponentCreator('/docs/soil-library/data_structures/predefined/object_ds','fd8'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/predefined/pd_data_frame',
  component: ComponentCreator('/docs/soil-library/data_structures/predefined/pd_data_frame','de0'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/streams/patients',
  component: ComponentCreator('/docs/soil-library/data_structures/streams/patients','3f2'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/streams/stream',
  component: ComponentCreator('/docs/soil-library/data_structures/streams/stream','0d0'),
  exact: true,
},
{
  path: '/docs/soil-library/data_structures/streams/trajectory_clusters',
  component: ComponentCreator('/docs/soil-library/data_structures/streams/trajectory_clusters','5fd'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/clustering/NBClustering',
  component: ComponentCreator('/docs/soil-library/modules/clustering/NBClustering','606'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/clustering/NBClustering_categorical',
  component: ComponentCreator('/docs/soil-library/modules/clustering/NBClustering_categorical','9dd'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/clustering/SIDIWO/sidiwo',
  component: ComponentCreator('/docs/soil-library/modules/clustering/SIDIWO/sidiwo','eae'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/experiment',
  component: ComponentCreator('/docs/soil-library/modules/experiment','b22'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/higher_order/Predictor',
  component: ComponentCreator('/docs/soil-library/modules/higher_order/Predictor','a9a'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/itemsets/frequent_itemsets_compare',
  component: ComponentCreator('/docs/soil-library/modules/itemsets/frequent_itemsets_compare','e06'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/itemsets/frequent_itemsets_hypergraph',
  component: ComponentCreator('/docs/soil-library/modules/itemsets/frequent_itemsets_hypergraph','382'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/preprocessing/filters/events_filter',
  component: ComponentCreator('/docs/soil-library/modules/preprocessing/filters/events_filter','ac4'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/preprocessing/filters/row_filter',
  component: ComponentCreator('/docs/soil-library/modules/preprocessing/filters/row_filter','6ac'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/statistics/customstatistics',
  component: ComponentCreator('/docs/soil-library/modules/statistics/customstatistics','4c4'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/statistics/time_statistics',
  component: ComponentCreator('/docs/soil-library/modules/statistics/time_statistics','5b3'),
  exact: true,
},
{
  path: '/docs/soil-library/modules/temporal/trajectories',
  component: ComponentCreator('/docs/soil-library/modules/temporal/trajectories','fb3'),
  exact: true,
},
{
  path: '/docs/tutorial/alerts',
  component: ComponentCreator('/docs/tutorial/alerts','e9b'),
  exact: true,
},
{
  path: '/docs/tutorial/data',
  component: ComponentCreator('/docs/tutorial/data','acb'),
  exact: true,
},
{
  path: '/docs/tutorial/data-structures',
  component: ComponentCreator('/docs/tutorial/data-structures','ecc'),
  exact: true,
},
{
  path: '/docs/tutorial/deployments',
  component: ComponentCreator('/docs/tutorial/deployments','4f7'),
  exact: true,
},
{
  path: '/docs/tutorial/get-started',
  component: ComponentCreator('/docs/tutorial/get-started','ffc'),
  exact: true,
},
{
  path: '/docs/tutorial/logging',
  component: ComponentCreator('/docs/tutorial/logging','d10'),
  exact: true,
},
{
  path: '/docs/tutorial/modules',
  component: ComponentCreator('/docs/tutorial/modules','7c8'),
  exact: true,
},
{
  path: '/docs/tutorial/scripts',
  component: ComponentCreator('/docs/tutorial/scripts','566'),
  exact: true,
},
]
},
{
  path: '*',
  component: ComponentCreator('*')
}
];
