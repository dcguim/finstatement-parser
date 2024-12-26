from typing import Optional
from pydantic import BaseModel, Field, root_validator

# Current Assets
class CurrentAssets(BaseModel):
    cash_and_cash_equivalents: Optional[float] = Field(
        0.0,
        description="Assets: Liquid assets including currency, bank balances, and highly liquid investments with maturities of three months or less.",
        fin_type='asset'
    )
    accounts_receivable: Optional[float] = Field(
        0.0,
        description="Assets: Amounts owed to the company by customers for goods or services delivered on credit.",
        fin_type='asset'
    )
    inventory: Optional[float] = Field(
        0.0,
        description="Assets: The value of goods available for sale or raw materials used in production.",
        fin_type='asset'
    )
    prepaid_expenses: Optional[float] = Field(
        0.0,
        description="Assets: Payments made in advance for goods or services to be received in the future.",
        fin_type='asset'
    )
    short_term_investments: Optional[float] = Field(
        0.0,
        description="Assets: Investments intended to be sold or converted into cash within a year.",
        fin_type='asset'
    )
    total_current_assets: float = Field(
        None,
        description="Assets: The total value of all current assets.",
        fin_type='asset'
    )

    @root_validator(pre=True)
    def ensure_total_current_assets(cls, values):
        if values.get('total_current_assets') is None:
            values['total_current_assets'] = (
                values.get('cash_and_cash_equivalents', 0) +
                values.get('accounts_receivable', 0) +
                values.get('inventory', 0) +
                values.get('prepaid_expenses', 0) +
                values.get('short_term_investments', 0)
            )
        return values

# Long-Term Assets
class LongTermAssets(BaseModel):
    property_plant_equipment: Optional[float] = Field(
        0.0,
        description="Assets: Tangible fixed assets used in operations, including buildings, machinery, and land.",
        fin_type='asset'
    )
    intangible_assets: Optional[float] = Field(
        0.0,
        description="Assets: Non-physical assets such as patents, trademarks, and goodwill.",
        fin_type='asset'
    )
    long_term_investments: Optional[float] = Field(
        0.0,
        description="Assets: Investments not intended to be sold within the next year, such as stocks, bonds, or real estate.",
        fin_type='asset'
    )
    deferred_tax_assets: Optional[float] = Field(
        0.0,
        description="Assets: Future tax benefits arising from temporary differences between accounting and tax bases.",
        fin_type='asset'
    )
    other_non_current_assets: Optional[float] = Field(
        0.0,
        description="Assets: Any other assets not classified as current or specifically listed, often miscellaneous items.",
        fin_type='asset'
    )
    total_long_term_assets: float = Field(
        None,
        description="Assets: The total value of all long-term assets.",
        fin_type='asset'
    )

    @root_validator(pre=True)
    def ensure_total_long_term_assets(cls, values):
        if values.get('total_long_term_assets') is None:
            values['total_long_term_assets'] = (
                values.get('property_plant_equipment', 0) +
                values.get('intangible_assets', 0) +
                values.get('long_term_investments', 0) +
                values.get('deferred_tax_assets', 0) +
                values.get('other_non_current_assets', 0)
            )
        return values

# Current Liabilities
class CurrentLiabilities(BaseModel):
    accounts_payable: Optional[float] = Field(
        0.0,
        description="Liability: Obligations to suppliers for goods or services received but not yet paid.",
        fin_type='liability'
    )
    short_term_loans: Optional[float] = Field(
        0.0,
        description="Liability: Borrowings due within one year.",
        fin_type='liability'
    )
    accrued_expenses: Optional[float] = Field(
        0.0,
        description="Liability: Expenses incurred but not yet paid, such as wages or utilities.",
        fin_type='liability'
    )
    deferred_revenue: Optional[float] = Field(
        0.0,
        description="Liability: Revenue received in advance for goods or services not yet delivered.",
        fin_type='liability'
    )
    current_portion_of_long_term_debt: Optional[float] = Field(
        0.0,
        description="Liability: The portion of long-term debt due within the next year.",
        fin_type='liability'
    )
    total_current_liabilities: float = Field(
        None,
        description="Liability: The total value of all current liabilities.",
        fin_type='liability'
    )

    @root_validator(pre=True)
    def ensure_total_current_liabilities(cls, values):
        if values.get('total_current_liabilities') is None:
            values['total_current_liabilities'] = (
                values.get('accounts_payable', 0) +
                values.get('short_term_loans', 0) +
                values.get('accrued_expenses', 0) +
                values.get('deferred_revenue', 0) +
                values.get('current_portion_of_long_term_debt', 0)
            )
        return values

# Long-Term Liabilities
class LongTermLiabilities(BaseModel):
    long_term_debt: Optional[float] = Field(
        0.0,
        description="Liability: Borrowings not due within the next year, such as bonds or loans.",
        fin_type='liability'
    )
    deferred_tax_liabilities: Optional[float] = Field(
        0.0,
        description="Liability: Taxes owed in the future due to temporary differences between accounting and tax bases.",
        fin_type='liability'
    )
    pension_liabilities: Optional[float] = Field(
        0.0,
        description="Liability: Obligations for employee retirement benefits.",
        fin_type='liability'
    )
    lease_liabilities: Optional[float] = Field(
        0.0,
        description="Liability: Obligations under long-term lease agreements.",
        fin_type='liability'
    )
    other_non_current_liabilities: Optional[float] = Field(
        0.0,
        description="Liability: Miscellaneous obligations not classified as current or specifically listed.",
        fin_type='liability'
    )
    total_long_term_liabilities: float = Field(
        None,
        description="Liability: The total value of all long-term liabilities.",
        fin_type='liability'
    )

    @root_validator(pre=True)
    def ensure_total_long_term_liabilities(cls, values):
        if values.get('total_long_term_liabilities') is None:
            values['total_long_term_liabilities'] = (
                values.get('long_term_debt', 0) +
                values.get('deferred_tax_liabilities', 0) +
                values.get('pension_liabilities', 0) +
                values.get('lease_liabilities', 0) +
                values.get('other_non_current_liabilities', 0)
            )
        return values

# Equity
class Equity(BaseModel):
    common_stock: Optional[float] = Field(
        0.0,
        description="Equity: The value of shares issued by the company to shareholders.",
        fin_type='equity'
    )
    retained_earnings: Optional[float] = Field(
        0.0,
        description="Equity: Cumulative net income retained for reinvestment in the business rather than distributed as dividends.",
        fin_type='equity'
    )
    additional_paid_in_capital: Optional[float] = Field(
        0.0,
        description="Equity: Excess amounts paid by investors over the par value of issued stock.",
        fin_type='equity'
    )
    treasury_stock: Optional[float] = Field(
        0.0,
        description="Equity: The value of shares repurchased by the company and held in its treasury.",
        fin_type='equity'
    )
    total_equity: float = Field(
        None,
        description="Equity: The total value of all equity accounts.",
        fin_type='equity'
    )

    @root_validator(pre=True)
    def ensure_total_equity(cls, values):
        if values.get('total_equity') is None:
            values['total_equity'] = (
                values.get('common_stock', 0) +
                values.get('retained_earnings', 0) +
                values.get('additional_paid_in_capital', 0) -
                values.get('treasury_stock', 0)
            )
        return values

class BalanceStatement(BaseModel):
    current_assets: CurrentAssets
    long_term_assets: LongTermAssets
    current_liabilities: CurrentLiabilities
    long_term_liabilities: LongTermLiabilities
    equity: Equity

    total_assets: float = Field(
        None,
        description="Assets: The total assets, calculated as the sum of current and long-term assets.",
        fin_type='asset'
    )
    total_liabilities: float = Field(
        None,
        description="Liability: The total liabilities, calculated as the sum of current and long-term liabilities.",
        fin_type='liability'
    )
    total_equity: float = Field(
        None,
        description="Equity: The total equity, obtained from the Equity instance.",
        fin_type='equity'
    )
    total_liabilities_and_equity: float = Field(
        None,
        description="Equity: The total of liabilities and equity, which should match the total assets.",
        fin_type='equity'
    )

    @root_validator(pre=True)
    def ensure_total_assets(cls, values):
        """
        Calculates total assets as the sum of current assets and long-term assets.
        """
        if values.get('total_assets') is None:
            values['total_assets'] = (
                values['current_assets'].total_current_assets +
                values['long_term_assets'].total_long_term_assets
            )
        return values

    @root_validator(pre=True)
    def ensure_total_liabilities(cls, values):
        """
        Calculates total liabilities as the sum of current liabilities and long-term liabilities.
        """
        if values.get('total_liabilities') is None:
            values['total_liabilities'] = (
                values['current_liabilities'].total_current_liabilities +
                values['long_term_liabilities'].total_long_term_liabilities
            )
        return values

    @root_validator(pre=True)
    def ensure_total_equity(cls, values):
        """
        Retrieves total equity from the Equity instance.
        """
        if values.get('total_equity') is None:
            values['total_equity'] = values['equity'].total_equity
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_total_liabilities_and_equity(cls, values):
        """
        Calculates total liabilities and equity and ensures it matches total assets.
        """
        # Ensure previous calculations for total liabilities and equity
        values = cls.ensure_total_liabilities(values)
        values = cls.ensure_total_equity(values)

        # Calculate total liabilities and equity
        if values.get('total_liabilities_and_equity') is None:
            values['total_liabilities_and_equity'] = (
                values['total_liabilities'] +
                values['total_equity']
            )

        # Check if total assets match total liabilities and equity
        if 'total_assets' not in values:
            values = cls.ensure_total_assets(values)
        assert values['total_assets'] == values['total_liabilities_and_equity'], (
            "Total assets do not match total liabilities and equity."
        )
        return values

class BalanceStatement(BaseModel):
    current_assets: CurrentAssets
    long_term_assets: LongTermAssets
    current_liabilities: CurrentLiabilities
    long_term_liabilities: LongTermLiabilities
    equity: Equity

    total_assets: float = Field(
        None,
        description="The total assets, calculated as the sum of current and long-term assets.",
        fin_type='asset'
    )
    total_liabilities: float = Field(
        None,
        description="The total liabilities, calculated as the sum of current and long-term liabilities.",
        fin_type='liability'
    )
    total_equity: float = Field(
        None,
        description="The total equity, obtained from the Equity instance.",
        fin_type='liability'
    )

    @root_validator(pre=True)
    def ensure_total_assets(cls, values):
        """
        Calculates total assets as the sum of current assets and long-term assets.
        """
        if values.get('total_assets') is None:
            values['total_assets'] = (
                values['current_assets'].total_current_assets +
                values['long_term_assets'].total_long_term_assets
            )
        return values

    @root_validator(pre=True)
    def ensure_total_liabilities(cls, values):
        """
        Calculates total liabilities as the sum of current liabilities and long-term liabilities.
        """
        if values.get('total_liabilities') is None:
            values['total_liabilities'] = (
                values['current_liabilities'].total_current_liabilities +
                values['long_term_liabilities'].total_long_term_liabilities
            )
        return values

    @root_validator(pre=True)
    def ensure_total_equity(cls, values):
        """
        Retrieves total equity from the Equity instance.
        """
        if values.get('total_equity') is None:
            values['total_equity'] = values['equity'].total_equity
        return values

    @root_validator(pre=False, skip_on_failure=True)
    def ensure_total_liabilities_and_equity(cls, values):
        """
        Calculates total liabilities and equity and ensures it matches total assets.
        """
        # Ensure previous calculations for total liabilities and equity
        values = cls.ensure_total_liabilities(values)
        values = cls.ensure_total_equity(values)

        # Check if total assets match total liabilities and equity
        if 'total_assets' not in values:
            values = cls.ensure_total_assets(values)

        return values

if __name__ == '__main__':
    print('1. Testing Current Assets Calculations')
    current_assets1 = CurrentAssets(
        cash_and_cash_equivalents=10000,
        accounts_receivable=5000,
        inventory=8000,
        prepaid_expenses=2000,
        short_term_investments=3000
    )
    print(f'\n> total current assets test1: {current_assets1.total_current_assets}')
    
    current_assets2 = CurrentAssets(
        cash_and_cash_equivalents=1500,
        total_current_assets=25000
    )
    print(f'\n> total current assets test2: {current_assets2.total_current_assets}')

    current_assets3 = CurrentAssets(
        total_current_assets=50000
    )
    print(f'\n> total current assets test3: {current_assets3.total_current_assets}')

    print('\n2. Testing Long-Term Assets Calculations')
    long_term_assets1 = LongTermAssets(
        property_plant_equipment=25000,
        intangible_assets=5000,
        long_term_investments=10000,
        deferred_tax_assets=2000,
        other_non_current_assets=3000
    )
    print(f'\n> total long-term assets test1: {long_term_assets1.total_long_term_assets}')
    
    long_term_assets2 = LongTermAssets(
        property_plant_equipment=4000,
        total_long_term_assets=30000
    )
    print(f'\n> total long-term assets test2: {long_term_assets2.total_long_term_assets}')

    print('\n3. Testing Current Liabilities Calculations')
    current_liabilities1 = CurrentLiabilities(
        accounts_payable=5000,
        short_term_loans=2000,
        accrued_expenses=1500,
        deferred_revenue=3000,
        current_portion_of_long_term_debt=1000
    )
    print(f'\n> total current liabilities test1: {current_liabilities1.total_current_liabilities}')
    
    current_liabilities2 = CurrentLiabilities(
        total_current_liabilities=15000
    )
    print(f'\n> total current liabilities test2: {current_liabilities2.total_current_liabilities}')

    print('\n4. Testing Long-Term Liabilities Calculations')
    long_term_liabilities1 = LongTermLiabilities(
        long_term_debt=30000,
        deferred_tax_liabilities=2000,
        pension_liabilities=5000,
        lease_liabilities=3000,
        other_non_current_liabilities=1000
    )
    print(f'\n> total long-term liabilities test1: {long_term_liabilities1.total_long_term_liabilities}')
    
    long_term_liabilities2 = LongTermLiabilities(
        long_term_debt=15000,
        total_long_term_liabilities=35000
    )
    print(f'\n> total long-term liabilities test2: {long_term_liabilities2.total_long_term_liabilities}')

    print('\n5. Testing Equity Calculations')
    equity1 = Equity(
        common_stock=20000,
        retained_earnings=10000,
        additional_paid_in_capital=5000,
        treasury_stock=2000
    )
    print(f'\n> total equity test1: {equity1.total_equity}')
    
    equity2 = Equity(
        total_equity=40000
    )
    print(f'\n> total equity test2: {equity2.total_equity}')
    # test balance statement total assets calculation
    current_assets = CurrentAssets(total_current_assets=50000)
    long_term_assets = LongTermAssets(total_long_term_assets=150000)
    current_liabilities = CurrentLiabilities(total_current_liabilities=30000)
    long_term_liabilities = LongTermLiabilities(total_long_term_liabilities=100000)
    equity = Equity(total_equity=70000)

    balance_stmt = BalanceStatement(
        current_assets=current_assets,
        long_term_assets=long_term_assets,
        current_liabilities=current_liabilities,
        long_term_liabilities=long_term_liabilities,
        equity=equity
    )

    print(f'\n> Balance Statement Test 1:\n'
          f'  Current Assets: {balance_stmt.current_assets.total_current_assets}\n'
          f'  Long-Term Assets: {balance_stmt.long_term_assets.total_long_term_assets}\n'
          f'  ===============================\n'
          f'  Total Assets: {balance_stmt.total_assets}\n')

    assert balance_stmt.total_assets == 200000, "Total assets calculation failed."


    # test balance statement total liabilities calculation
    current_assets = CurrentAssets(total_current_assets=50000)
    long_term_assets = LongTermAssets(total_long_term_assets=150000)
    current_liabilities = CurrentLiabilities(total_current_liabilities=30000)
    long_term_liabilities = LongTermLiabilities(total_long_term_liabilities=120000)
    equity = Equity(total_equity=70000)

    balance_stmt = BalanceStatement(
        current_assets=current_assets,
        long_term_assets=long_term_assets,
        current_liabilities=current_liabilities,
        long_term_liabilities=long_term_liabilities,
        equity=equity
    )

    print(f'\n> Balance Statement Test 2:\n'
          f'  Current Liabilities: {balance_stmt.current_liabilities.total_current_liabilities}\n'
          f'  Long-Term Liabilities: {balance_stmt.long_term_liabilities.total_long_term_liabilities}\n'
          f'  ===============================\n'
          f'  Total Liabilities: {balance_stmt.total_liabilities}\n')

    assert balance_stmt.total_liabilities == 150000, "Total liabilities calculation failed."


    # test balance statement balance check
    current_assets = CurrentAssets(total_current_assets=60000)
    long_term_assets = LongTermAssets(total_long_term_assets=140000)
    current_liabilities = CurrentLiabilities(total_current_liabilities=40000)
    long_term_liabilities = LongTermLiabilities(total_long_term_liabilities=80000)
    equity = Equity(total_equity=80000)

    balance_stmt = BalanceStatement(
        current_assets=current_assets,
        long_term_assets=long_term_assets,
        current_liabilities=current_liabilities,
        long_term_liabilities=long_term_liabilities,
        equity=equity
    )

    print(f'\n> Balance Statement Test 3:\n'
          f'  Total Assets: {balance_stmt.total_assets}\n'
          f'  Total Liabilities: {balance_stmt.total_liabilities}\n'
          f'  Total Equity: {balance_stmt.total_equity}\n'
          f'  ===============================\n'
          f'  Total Liabilities & Equity: {balance_stmt.total_liabilities + balance_stmt.total_equity}\n')

    assert balance_stmt.total_assets == (balance_stmt.total_liabilities + balance_stmt.total_equity), (
        "Total assets do not match total liabilities and equity."
    )

