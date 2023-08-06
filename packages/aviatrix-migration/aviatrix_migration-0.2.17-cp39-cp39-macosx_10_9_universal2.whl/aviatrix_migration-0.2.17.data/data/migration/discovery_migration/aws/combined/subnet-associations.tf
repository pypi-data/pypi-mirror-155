resource "aws_route_table_association" "$rname" {
  subnet_id      = $subnet_id_ref
  route_table_id = $route_table_id_ref
  provider       = $provider
}
