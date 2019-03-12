var page_list = [index_page, graph_page, database_page, component_page, deeplearning_page];
function change_page(page_name) {
  for (var i in page_list) {
    page_list[i].visi = page_name;
  }
}
