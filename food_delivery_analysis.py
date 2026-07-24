import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class FoodDeliveryAnalysis:
    """
    A class to perform analysis on the Online Food Delivery Database.
    Loads CSV data and performs various analytics operations.
    """
    
    def __init__(self, data_path: str = './data/'):
        """
        Initialize the analysis with data path.
        
        Args:
            data_path: Path to the directory containing CSV files
        """
        self.data_path = data_path
        self.restaurants = None
        self.menus = None
        self.customers = None
        self.orders = None
        self.delivery_agents = None
        
        # Load all data
        self.load_data()
    
    def load_data(self):
        """Load all CSV files into DataFrames"""
        try:
            self.restaurants = pd.read_csv(f'{self.data_path}restaurants Table.csv')
            self.menus = pd.read_csv(f'{self.data_path}menus Table.csv')
            self.customers = pd.read_csv(f'{self.data_path}customers Table.csv')
            self.orders = pd.read_csv(f'{self.data_path}orders Table1.csv')
            self.delivery_agents = pd.read_csv(f'{self.data_path}delivery_agents Table.csv')
            
            print("✓ All data loaded successfully")
            self.display_data_summary()
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
    
    def display_data_summary(self):
        """Display summary of all loaded datasets"""
        print("\n" + "="*50)
        print("DATA SUMMARY")
        print("="*50)
        print(f"Restaurants: {len(self.restaurants)} records")
        print(f"Menus: {len(self.menus)} records")
        print(f"Customers: {len(self.customers)} records")
        print(f"Orders: {len(self.orders)} records")
        print(f"Delivery Agents: {len(self.delivery_agents)} records")
        print("="*50 + "\n")
    
    # ============= ANALYSIS QUERIES =============
    
    def top_3_food_items_by_sales(self) -> pd.DataFrame:
        """
        Query 01: Top 3 Food items by sales
        
        Returns:
            DataFrame with item names and total sales
        """
        # Merge orders with menus using restaurant_id as connector
        merged = self.orders.merge(
            self.menus,
            left_on='restaurant_id',
            right_on='restaurant_id',
            how='inner'
        )
        
        # Group by item and sum sales
        result = merged.groupby('item_name')['total'].sum().reset_index()
        result.columns = ['item_name', 'total_sold']
        result = result.sort_values('total_sold', ascending=False).head(3)
        
        return result
    
    def delivery_vs_cancelled_orders(self) -> pd.DataFrame:
        """
        Query 02: Count of delivery vs cancelled orders
        Breakdown of orders by status
        
        Returns:
            DataFrame with status and count of orders
        """
        valid_statuses = ['Delivered', 'Cancelled', 'Out for Delivery', 'Preparing', 'Pending']
        
        result = self.orders[self.orders['status'].isin(valid_statuses)].groupby('status').size().reset_index(name='total_orders')
        result = result.sort_values('total_orders', ascending=False)
        
        return result
    
    def restaurants_with_most_orders(self) -> pd.DataFrame:
        """
        Query 03: List restaurants with most orders
        
        Returns:
            DataFrame with restaurant info and order count
        """
        result = self.orders.merge(
            self.restaurants,
            left_on='restaurant_id',
            right_on='id',
            how='inner'
        ).groupby(['id', 'name']).size().reset_index(name='total_orders')
        
        result.columns = ['restaurant_id', 'restaurant_name', 'total_orders']
        result = result.sort_values('total_orders', ascending=False).head(3)
        
        return result
    
    def assign_delivery_agent(self) -> pd.DataFrame:
        """
        Query 04: Assign delivery agent (join orders with agent)
        Join orders with delivery agents
        
        Returns:
            DataFrame with orders and assigned delivery agents
        """
        result = self.orders.merge(
            self.delivery_agents,
            left_on='id',
            right_on='id',
            how='inner',
            suffixes=('_order', '_agent')
        )
        
        result = result[['id', 'customer_id', 'restaurant_id', 'id_agent', 
                         'name_agent', 'status_agent', 'status_order']]
        result.columns = ['order_id', 'customer_id', 'restaurant_id', 
                         'agent_id', 'delivery_agent_name', 'agent_status', 'order_status']
        
        return result
    
    def revenue_per_restaurant(self) -> pd.DataFrame:
        """
        Query 05: Revenue per restaurant
        Calculate total revenue for each restaurant
        
        Returns:
            DataFrame with restaurant info and total revenue
        """
        result = self.orders.merge(
            self.restaurants,
            left_on='restaurant_id',
            right_on='id',
            how='inner'
        ).groupby(['id', 'name']).agg({'total': 'sum'}).reset_index()
        
        result.columns = ['restaurant_id', 'restaurant_name', 'total_revenue']
        result = result.sort_values('total_revenue', ascending=False)
        
        return result
    
    # ============= VISUALIZATION METHODS =============
    
    def plot_top_items(self):
        """Visualize top 3 food items by sales"""
        data = self.top_3_food_items_by_sales()
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(data['item_name'], data['total_sold'], color='steelblue', edgecolor='black')
        plt.title('Top 3 Food Items by Sales', fontsize=14, fontweight='bold')
        plt.xlabel('Item Name', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('top_3_items.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_order_status_distribution(self):
        """Visualize order status distribution"""
        data = self.delivery_vs_cancelled_orders()
        
        colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#95a5a6']
        plt.figure(figsize=(10, 6))
        plt.pie(data['total_orders'], labels=data['status'], autopct='%1.1f%%',
                colors=colors, startangle=90, explode=[0.05]*len(data))
        plt.title('Order Status Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('order_status_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_restaurants_by_orders(self):
        """Visualize top restaurants by order count"""
        data = self.restaurants_with_most_orders()
        
        plt.figure(figsize=(10, 6))
        bars = plt.barh(data['restaurant_name'], data['total_orders'], color='coral', edgecolor='black')
        plt.title('Top Restaurants by Order Count', fontsize=14, fontweight='bold')
        plt.xlabel('Total Orders', fontsize=12)
        plt.ylabel('Restaurant Name', fontsize=12)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}', ha='left', va='center', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        plt.savefig('top_restaurants.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_revenue_per_restaurant(self):
        """Visualize revenue per restaurant"""
        data = self.revenue_per_restaurant()
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(data['restaurant_name'], data['total_revenue'], 
                       color='mediumseagreen', edgecolor='black')
        plt.title('Total Revenue Per Restaurant', fontsize=14, fontweight='bold')
        plt.xlabel('Restaurant Name', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('revenue_per_restaurant.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # ============= STATISTICAL ANALYSIS =============
    
    def get_order_statistics(self) -> Dict:
        """Calculate statistics about orders"""
        stats = {
            'total_orders': len(self.orders),
            'total_revenue': self.orders['total'].sum(),
            'average_order_value': self.orders['total'].mean(),
            'median_order_value': self.orders['total'].median(),
            'max_order_value': self.orders['total'].max(),
            'min_order_value': self.orders['total'].min(),
            'std_dev_order_value': self.orders['total'].std()
        }
        return stats
    
    def get_customer_insights(self) -> Dict:
        """Get insights about customers"""
        order_per_customer = self.orders.groupby('customer_id').size()
        
        insights = {
            'total_customers': len(self.customers),
            'customers_who_ordered': len(order_per_customer),
            'avg_orders_per_customer': order_per_customer.mean(),
            'max_orders_by_customer': order_per_customer.max(),
            'repeat_customers': len(order_per_customer[order_per_customer > 1])
        }
        return insights
    
    def print_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*60)
        print("ONLINE FOOD DELIVERY - COMPREHENSIVE ANALYSIS REPORT")
        print("="*60)
        
        # Query 1: Top 3 Items
        print("\n[QUERY 01] TOP 3 FOOD ITEMS BY SALES")
        print("-" * 60)
        print(self.top_3_food_items_by_sales().to_string(index=False))
        
        # Query 2: Order Status
        print("\n[QUERY 02] ORDER STATUS DISTRIBUTION")
        print("-" * 60)
        print(self.delivery_vs_cancelled_orders().to_string(index=False))
        
        # Query 3: Top Restaurants
        print("\n[QUERY 03] TOP 3 RESTAURANTS BY ORDER COUNT")
        print("-" * 60)
        print(self.restaurants_with_most_orders().to_string(index=False))
        
        # Query 4: Delivery Assignment
        print("\n[QUERY 04] DELIVERY AGENT ASSIGNMENTS (First 5 rows)")
        print("-" * 60)
        print(self.assign_delivery_agent().head().to_string(index=False))
        
        # Query 5: Revenue
        print("\n[QUERY 05] REVENUE PER RESTAURANT")
        print("-" * 60)
        print(self.revenue_per_restaurant().to_string(index=False))
        
        # Statistics
        print("\n[STATISTICS] ORDER STATISTICS")
        print("-" * 60)
        stats = self.get_order_statistics()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: ${value:.2f}" if 'revenue' in key or 'value' in key else f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        
        # Customer Insights
        print("\n[INSIGHTS] CUSTOMER INSIGHTS")
        print("-" * 60)
        insights = self.get_customer_insights()
        for key, value in insights.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main function to run the analysis"""
    
    # Initialize analysis (update path to your data directory)
    analysis = FoodDeliveryAnalysis(data_path='./data/')
    
    # Print comprehensive report
    analysis.print_report()
    
    # Generate visualizations
    print("Generating visualizations...")
    analysis.plot_top_items()
    analysis.plot_order_status_distribution()
    analysis.plot_restaurants_by_orders()
    analysis.plot_revenue_per_restaurant()
    print("Visualizations saved successfully!")
    
    # Export results to CSV
    print("\nExporting results...")
    analysis.top_3_food_items_by_sales().to_csv('analysis_top_items.csv', index=False)
    analysis.delivery_vs_cancelled_orders().to_csv('analysis_order_status.csv', index=False)
    analysis.restaurants_with_most_orders().to_csv('analysis_top_restaurants.csv', index=False)
    analysis.revenue_per_restaurant().to_csv('analysis_revenue.csv', index=False)
    print("Results exported to CSV files!")


if __name__ == "__main__":
    main()
