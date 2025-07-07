export interface Company {
  id: number;
  Company: string;
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
  Company: string;
  code: string;
  description?: string;
  is_active?: boolean;
}

export interface CompanyUpdate {
  Company?: string;
  code?: string;
  description?: string;
  is_active?: boolean;
} 