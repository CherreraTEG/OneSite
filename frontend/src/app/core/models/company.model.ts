export interface Company {
  id: number;
  name: string;
  code: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CompanyList {
  companies: Company[];
  total: number;
}

export interface CompanyCreate {
  name: string;
  code: string;
  description?: string;
  is_active?: boolean;
}

export interface CompanyUpdate {
  name?: string;
  code?: string;
  description?: string;
  is_active?: boolean;
} 