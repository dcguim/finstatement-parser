from pydantic import BaseModel, Field, root_validator
from typing import Optional

class COGS(BaseModel):
    raw_materials_cost: Optional[float] = Field(
        0.0,
        description="Expense: The cost of raw materials directly used in production; classified as a cost within the Cost of Goods Sold.",
        fin_type='expense'
    )
    labor_cost: Optional[float] = Field(
        0.0, 
        description="Expense: All expenses for wages and benefits of production staff; classified as a cost within the Cost of Goods Sold.",
        fin_type='expense'
    )
    manufacturing_overhead: Optional[float] = Field(
        0.0, 
        description="Expense: Indirect production expenses, such as utilities and equipment maintenance; classified as a cost within the Cost of Goods Sold.",
        fin_type='expense'
    )
    freight_and_shipping: Optional[float] = Field(
        0.0, 
        description="Expense: Costs for transporting goods to customers or facilities; classified as a cost within the Cost of Goods Sold.",
        fin_type='expense'
    )
    inventory_changes: Optional[float] = Field(
        0.0, 
        description="Expense: Adjustments in inventory value over the period; classified as a cost affecting the total within the Cost of Goods Sold.",
        fin_type='expense'
    )
    total_cogs: float = Field(
        None, 
        description="Expense: The combined total of all production costs, including materials, labor, and overhead; represents the full Cost of Goods Sold.",
        fin_type='expense'
    )

    @root_validator(pre=True)
    def ensure_cogs(cls, values):
        # Calculate total operating expenses if not provided
        if values.get('total_cogs') is None:
            # Summing all fields that contribute to operating expenses
            values['total_cogs'] = (
                values.get('raw_materials_cost', 0) +
                values.get('labor_cost', 0) +
                values.get('manufacturing_overhead', 0) +
                values.get('freight_and_shipping', 0) +
                values.get('inventory_changes', 0)
            )
        # Return the updated 'values' to ensure modifications persist
        return values

class OperatingExpenses(BaseModel):
    # Selling, General & Administrative Expenses (SG&A)
    sales_salaries: Optional[float] = Field(
        0.0,
        description="Expense: Salaries for the sales department, categorized within operational selling expenses.",
        fin_type='expense'
    )
    advertising_marketing: Optional[float] = Field(
        0.0,
        description="Expense: Costs within operational selling expenses for promoting products or services, covering advertising campaigns and marketing activities.",
        fin_type='expense'
)
    sales_commissions: Optional[float] = Field(
        0.0,
        description="Expense: Payments within operational selling expenses made to salespeople, typically as a percentage of sales generated.",
        fin_type='expense'
    )
    sales_travel: Optional[float] = Field(
        0.0,
        description="Expense: Travel expenses within operational selling expenses, incurred by sales staff for transportation, lodging, and meals.",
        fin_type='expense'
    )

    # General & Administrative Expenses (G&A)
    executive_salaries: Optional[float] = Field(
        0.0,
        description="Expense: Salaries for executives, classified within operational general and administrative expenses.",
        fin_type='expense'
    )
    office_rent_utilities: Optional[float] = Field(
        0.0,
        description="Expense: Costs for office rent and utilities, included within operational general and administrative expenses.",
        fin_type='expense'
    )
    accounting_fees: Optional[float] = Field(
        0.0,
        description="Expense: Fees for legal and accounting services, recorded within operational general and administrative expenses.",
        fin_type='expense'
    )
    insurance: Optional[float] = Field(
        0.0,
        description="Expense: Insurance expenses necessary for business operations, categorized within operational general and administrative expenses.",
        fin_type='expense'
)
    depreciation: Optional[float] = Field(
        0.0,
        description="Expense: Depreciation expenses for assets, listed within operational general and administrative expenses.",
        fin_type='expense'
    )
    amortization: Optional[float] = Field(
        0.0,
        description="Expense: Amortization expenses for intangible assets, considered part of operational general and administrative expenses.",
        fin_type='expense'
    )
    bad_debt: Optional[float] = Field(
        0.0,
        description="Expense: Write-offs for uncollectible accounts receivable, included within operational general and administrative expenses.",
        fin_type='expense'
    )
    consumables: Optional[float] = Field(
        0.0,
        description="Expense: General-purpose office consumables, recorded within operational general and administrative expenses.",
        fin_type='expense'
    )
    office_supplies: Optional[float] = Field(
        0.0,
        description="Expense: Costs for general office supplies, part of operational general and administrative expenses.",
        fin_type='expense'
    )
    professional_fees: Optional[float] = Field(
        0.0,
        description="Expense: Fees paid for consultancy or contractor services, classified within operational general and administrative expenses.",
        fin_type='expense'
    )
    permits_licenses_subscriptions: Optional[float] = Field(
        0.0,
        description="Expense: Costs for permits, licenses, and subscriptions, included within operational general and administrative expenses.",
        fin_type='expense'
    )
    freight_cartage_postage: Optional[float] = Field(
        0.0,
        description="Expense: Shipping costs related to general business operations, recorded within operational general and administrative expenses.",
        fin_type='expense'
    )
    hiring_fees: Optional[float] = Field(
        0.0,
        description="Expense: Fees for hiring and recruitment services, part of operational general and administrative expenses.",
        fin_type='expense'
    )

    total_sg_and_a: float = Field(
        None,
        description="Expense: The total cost of all operational selling, general, and administrative (SG&A) expenses.",
        fin_type='expense'
    )

    # Research & Development (R&D)
    r_and_d_salaries: Optional[float] = Field(
        0.0,        
        description="Expense: Salaries for employees in the research and development (R&D) department, included within operational R&D expenses.",
        fin_type='expense'
    )
    r_and_d_materials: Optional[float] = Field(
        0.0,
        description="Expense: Costs for materials used in research and development, categorized under operational R&D expenses.",
        fin_type='expense'
    )
    r_and_d_testing: Optional[float] = Field(
        0.0,
        description="Expense: Expenses for testing activities within research and development, part of operational R&D expenses.",
        fin_type='expense'
    )
    
    total_r_and_d: float = Field(
        None,
        description="Expense: The total cost of all operational research and development (R&D) expenses.",
        fin_type='expense'
    )

    # Other Operating Expenses
    maintenance_repairs: Optional[float] = Field(
        0.0,
        description="Expense: Expenses related to maintenance and repairs, categorized within other operational expenses.",
        fin_type='expense'
    )
    employee_benefits: Optional[float] = Field(
        0.0,
        description="Expense: Costs for employee benefits, such as health insurance and retirement contributions, included in other operational expenses.",
        fin_type='expense'
    )
    training_development: Optional[float] = Field(
        0.0,
        description="Expense: Expenses for employee training and development, considered part of other operational expenses.",
        fin_type='expense'
    )
    travel_meals: Optional[float] = Field(
        0.0,
        description="Expense: Travel and meals expenses for employees, classified within other operational expenses.",
        fin_type='expense'
    )
    impairment_costs: Optional[float] = Field(
        0.0,
        description="Expense: Losses incurred when the carrying value of an asset exceeds its recoverable amount, recognized within other operational expenses.",
        fin_type='expense'
    )
    donations: Optional[float] = Field(
        0.0,
        description="Expense: Charitable donations made by the company, recorded as part of other operational expenses.",
        fin_type='expense'
    )
    total_other_operating: float = Field(
        None,
        description="Expense: The total cost of all other operational expenses not classified under other specific categories.",
        fin_type='expense'
    )
    total_operating_expenses: float = Field(
        None,
        description="Expense: The total cost of all operating expenses, including selling, general and administrative expenses (SG&A), research and development (R&D) expenses, and other operational expenses.",
        fin_type='expense'
    )
    
    @root_validator(pre=True)
    def ensure_sg_and_a_expenses(cls, values):
        # Calculate total SG&A if not provided
        if values.get('total_sg_and_a') is None:
            # Summing all fields that contribute to operating expenses
            values['total_sg_and_a'] = (
                values.get('sales_salaries', 0) +
                values.get('advertising_marketing', 0) +
                values.get('sales_commissions', 0) +
                values.get('sales_travel', 0) +
                values.get('executive_salaries', 0) +
                values.get('office_rent_utilities', 0) +
                values.get('accounting_fees', 0) +
                values.get('insurance', 0) +
                values.get('depreciation', 0) +
                values.get('amortization', 0) +
                values.get('bad_debt', 0) +
                values.get('consumables', 0) +
                values.get('office_supplies', 0) +
                values.get('professional_fees', 0) +
                values.get('permits_licenses_subscriptions', 0) +
                values.get('freight_cartage_postage', 0)
            )
        # Return the updated 'values' to ensure modifications persist
        return values
    
    @root_validator(pre=True)
    def ensure_r_and_d_expenses(cls, values) -> float:
        # Calculate total R&D if not provided
        if values.get('total_r_and_d') is None:
            values['total_r_and_d'] = (
                values.get('r_and_d_salaries', 0) +
                values.get('r_and_d_materials', 0) +
                values.get('r_and_d_testing', 0)
            )
        return values

    @root_validator(pre=True)
    def ensure_total_other_operating_expenses(cls, values) -> float:
        # Calculate total R&D if not provided
        if values.get('total_other_operating') is None:
            values['total_other_operating'] = (
                values.get('maintenance_repairs', 0) +
                values.get('employee_benefits', 0) +
                values.get('training_development', 0) +
                values.get('travel_meals', 0) +
                values.get('impairment_costs', 0) +
                values.get('donations', 0) 
            )
        return values

    @root_validator(pre=True)
    def ensure_total_operating_expenses(cls, values) -> float:
        # Calculate total operating expenses if not provided
        values = cls.ensure_sg_and_a_expenses(values) if values.get('total_sg_and_a') is None else values
        values = cls.ensure_r_and_d_expenses(values) if values.get('total_r_and_d') is None else values
        values = cls.ensure_total_other_operating_expenses(values) if values.get('total_other_operating') is None else values
        if values.get('total_operating_expenses') is None:
            values['total_operating_expenses'] = (
                values.get('total_sg_and_a', 0) +
                values.get('total_r_and_d', 0) +
                values.get('total_other_operating', 0)
            )
        return values
    
class IncomeStatement(BaseModel):
    # Revenue (required field)
    revenue: float = Field(
        ...,
        description="Earnings: The total income generated by the company's core business activities, primarily through the sale of goods or services, before any expenses are deducted.",
        fin_type='earning')
    other_revenue: Optional[float] = Field(
        0.0,
        description="Earnings: Income generated from non-core business activities, such as interest income, gains on asset sales, or any other sources outside the primary operations of the business.",
        fin_type='earning')

    cogs: COGS

    operating_expenses: OperatingExpenses

    interest_expenses: Optional[float] = Field(
        0.0,
        description="Expenses: The cost incurred by the company from borrowing, including interest on loans and other debt-related obligations. Also called finance costs or debt expenses.",
        fin_type='expense')
    tax_expenses: float = Field(
        ...,
        description="Expeenses: The total amount of taxes the company is liable for, based on its earnings and applicable tax rates. Also referred to as income taxes or tax provision.",
        fin_type='expense')
    extraordinary_expenses: Optional[float] = Field(
        0.0,
        description="Expenses: One-time or infrequent expenses not expected to recur in the normal course of business, such as natural disaster costs or restructuring charges. Also known as non-recurring expenses or one-time expenses.",
        fin_type='expense')

    gross_profit: float = Field(
        None,
        description="Earnings: The difference between revenue and the cost of goods sold (COGS), showing how much the company earns from its core operations before accounting for operating expenses. Alternatively called gross margin or sales margin.",
        fin_type='earning')
    ebit: float = Field(
        None,
        description="Earnings: Earnings before interest and taxes; a measure of operating profit that excludes interest expenses and tax obligations, reflecting a company’s profitability from core operations. Also referred to as operating income or operating profit.",
        fin_type='earning')
    ebitda: float = Field(
        None,
        description="Earnings: Earnings before interest, taxes, depreciation, and amortization; a measure of a company’s operating performance that excludes the effects of financing and accounting decisions. Also called operating cash flow or earnings before interest, tax, depreciation, and amortization.",
        fin_type='earning')
    ebt: float = Field(
        None,
        description="Earnings: Earnings before tax; the company’s profit before accounting for taxes, showing how much it earned from all activities except taxes. Alternatively referred to as pre-tax profit or profit before tax.",
        fin_type='earning')
    net_income: float = Field(
        None,
        description="Earnings: The company’s final profit after all expenses, including operating costs, interest, taxes, and extraordinary items, have been deducted from revenue. Also known as net profit or bottom line.",
        fin_type='earning')
    total_expenses:float = Field(
        None,
        description="Expenses: The total costs incurred by the company during a specific period, including all operating expenses, interest expenses, tax expenses, and extraordinary items. Alternatively called total operating costs or total costs.",
        fin_type='expense')
    operating_margin:float = Field(
        None,
        description="Ratio: A profitability ratio that measures the percentage of revenue remaining after covering operating expenses, calculated as operating income divided by revenue. Also known as operating profit margin or operating income margin.",
                                   fin_type='ratio')
    net_margin:float = Field(
        None,
        description="Ratio: A profitability ratio that measures how much of each dollar of revenue remains as profit after all expenses (including operating costs, interest, and taxes) are deducted, calculated as net income divided by revenue. Alternatively called net profit margin or profit margin.",
        fin_type='ratio')
    
    @root_validator(pre=True)
    def ensure_gross_profit(cls, values) -> float:
        #print(values)
        # Calculate gross profit if not provided
        if values.get('gross_profit') is None:
            values['gross_profit'] = (
                values.get('revenue', 0) +
                values.get('other_revenue', 0) -
                values.get('cogs').total_cogs # this line could cause an error if the object doesn't exist!!!
            )
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_ebit(cls, values) ->  float:
        #print(values)
        values = cls.ensure_gross_profit(values ) if values.get('gross_profit') is None else values
        # Calculate EBIT if not provided
        if values.get('ebit') is None:
            values['ebit'] = (
                values.get('gross_profit') -
                values.get('operating_expenses').total_operating_expenses # this line could cause an error if the object doesn't exist!!!
            )
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_ebitda(cls, values) -> float:
        print('before fetching EBIT')
        print(values)
        values = ensure_ebit(values ) if values.get('ebit') is None else values
        print('after fetching EBIT')
        print(values)
        # Calculate EBITDA if not provided
        if values.get('ebitda') is None:
            values['ebitda'] = (
                values.get('ebit', 0) +
                values.get('operating_expenses').depreciation +
                values.get('operating_expenses').amortization # this line could cause an issue if the object doesn't exist!!!
            )
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_ebt(cls, values) -> float:
        #print(values)
        values = cls.ensure_ebit(values ) if values.get('ebit') is None else values
        # Calculate EBT if not provided
        if values.get('ebt') is None:
            values['ebt'] = (
                values.get('ebit', 0) -
                values.get('interest_expenses', 0)
            )
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_net_income(cls, values) -> float:
        #print(values)
        values = cls.ensure_ebt(values ) if values.get('ebt') is None else values
        # Calculate net income if not provided
        if values.get('net_income') is None:
            values['net_income'] = (
                values.get('ebt', 0) -
                values.get('tax_expenses', 0) +
                values.get('extraordinary_expenses', 0)
            )
        return values
    
    @root_validator(pre=False, skip_on_failure=True)
    def ensure_total_expenses(cls, values) -> float:
        #print(values)
        # by ensuring net income, I also insure ebt
        values = cls.ensure_net_income(values) if values.get('net_income') is None else values
        # Calculate total recurring and non-recurring expenses if not provided
        if values.get('total_expenses') is None:
            values['total_expenses'] = (
                values.get('cogs').total_cogs +
                values.get('operating_expenses').total_operating_expenses +
                values.get('interest_expenses', 0) +
                values.get('tax_expenses', 0) + 
                values.get('extraordinary_expenses', 0)
            )
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_operating_margin(cls, values) -> float:
        #print(values)
        values = cls.ensure_ebit(values) if values.get('ebit') is None else values
        # Calculate total operating margin if not provided
        if values.get('operating_margin') is None:
            values['operating_margin'] = (
                values.get('ebit', 0) /
                values.get('revenue', 0) if values.get('revenue', 0) else 0.0
            )
        return values
    
    @root_validator(pre=False, skip_on_failure=True)
    def ensure_net_margin(cls, values) -> float:
        #print(values)
        values = cls.ensure_net_income(values) if values.get('net_income') is None else values
        # Calculate total operating margin if not provided
        if values.get('net_margin') is None:
            values['net_margin'] = (
                values.get('net_income', 0) /
                values.get('revenue', 0) if values.get('revenue', 0) else 0.0
            )
        return values

if __name__=='__main__':
    print('1. Testing COGS Calculations')
    cogs1 = COGS(
        raw_materials_cost=20000,
        labor_cost=15000,
        manufacturing_overhead=8000,
        freight_and_shipping=2000,
        inventory_changes=1000
    )
    print(f'\n> total cogs test1: {cogs1.total_cogs}')
    cogs2 = COGS(
        raw_materials_cost=800,
        total_cogs=34000
    )
    print(f'\n> total cogs test2: {cogs2.total_cogs}')
    cogs3 = COGS(
        total_cogs=84300
    )
    print(f'\n> total cogs test3: {cogs3.total_cogs}')
    print('\n2. Testing Opex Calculations')
    opex1 = OperatingExpenses(
      #  sales_salaries = None,
        advertising_marketing = 23,
        sales_commissions = 713,
        sales_travel = 8.9,
        executive_salaries = 799.0,
        office_rent_utilities = 0.0,
        bad_debt = 2.3,
      #  accounting_fees = None,
        insurance = 3,
        depreciation = 9.22,
        amortization = 17900,
      #  research_and_development = None,
        r_and_d_salaries = 22,
        r_and_d_materials = 32,
        r_and_d_testing = 223,
        maintenance_repairs = 0.0,
        employee_benefits = 2.3,
        impairment_costs = 323,
        training_development = 34,
        travel_meals = 334
    )
    print(f'\n> total cogs opex1:\n  SG&A: {opex1.total_sg_and_a}\n  R&D: {opex1.total_r_and_d}\n  Other: {opex1.total_other_operating}\n  ================\n  Total = {opex1.total_operating_expenses}')
    opex2 = OperatingExpenses(
        sales_salaries = 300,
        advertising_marketing = 23,
     #   sales_commissions = None,
        total_sg_and_a = 23000,
        sales_travel = 8.9,
        executive_salaries = 799.0,
        bad_debt =223,
        office_rent_utilities = 0.0,
        accounting_fees = 3,
        insurance = 3,
      #  depreciation = None,
        amortization = 17900,
        total_other_operating = 2600,
        research_and_development = 93,
        r_and_d_salaries = 22,
        r_and_d_materials = 32,
    #    r_and_d_testing = None,
        maintenance_repairs = 0.0,
        employee_benefits = 2.3,
        training_development = 34,
        travel_meals = 334,
        impairment_costs=223
    )
    print(f'\n> total cogs opex2:\n  SG&A: {opex2.total_sg_and_a}\n  R&D: {opex2.total_r_and_d}\n  Other: {opex2.total_other_operating}\n  ================\n  Total = {opex2.total_operating_expenses}')
    print('\n3. Testing Income Statement')
    incst1 = IncomeStatement(
        revenue = 148300,
        other_revenue = 0.0,
        cogs = cogs1,
        operating_expenses = opex1,
        # other expenses
        interest_expenses = 2300,
        tax_expenses = 78000,
        extraordinary_expenses = 230)
    print(f'\n> income statement 1:\n  Gross profit: {incst1.gross_profit}\n  EBITDA: {incst1.ebitda}\n  EBIT: {incst1.ebit}\n  EBT: {incst1.ebt}\n  Tax Expenses: ({incst1.tax_expenses})\n  Total other expenses: ({incst1.total_expenses})\n  ==================================\n  Net Income: {incst1.net_income}\n  Operating Margin: {incst1.operating_margin} %\n  Net Margin: {incst1.net_margin} %\n')
    print('=================================')
    print('Example with Leigh\'s income statement:')
    cogs_leigh = COGS(
        total_cogs = 844.4
    )
    opex_leigh = OperatingExpenses(
        sales_salaries = 0,
        advertising_marketing = 417,
        sales_commissions = 0,
        total_sg_and_a = 0,
        sales_travel = 0,
        impairment_cost = 1690,
        executive_salaries = 0,
        office_rent_utilities = 0,
        office_supplies=35, 
        consumables = 56, 
        it_costs = 87, 
        accounting_fees = 750,
        professional_fees = 0,
        permits_licenses_subscriptions = 0,
        insurance = 0,
        depreciation = 0,
        amortization = 0,
        total_other_operating = 0,
        research_and_development = 0,
        r_and_d_salaries = 0,
        r_and_d_materials = 0,
        r_and_d_testing = 0,
        maintenance_repairs = 0,
        employee_benefits = 0,
        training_development = 0,
        donations = 3, 
        freight_cartage_postage = 234,
        hiring_fees=2700, 
        travel_meals = 0
    )

