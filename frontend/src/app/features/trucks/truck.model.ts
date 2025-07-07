export interface Truck {
  id?: number;
  id_empresa: number;
  id_warehouse: number;
  ship_date?: string;
  deliv_date?: string;
  carrier?: string;
  customer_facility?: string;
  po?: string;
  qty?: number;
  estatus?: number;
  time_in?: string;
  door?: string;
  time_out?: string;
  comments?: string;
  pickup_location?: string;
  load_number?: string;
  id_customer?: number;
  estado_cargue?: number;
  update_date?: string;
  update_user?: string;
  file_name?: string;
} 