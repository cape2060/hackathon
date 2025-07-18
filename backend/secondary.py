import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('realistic_shoe_company_data.csv')
# Group by product_niche and sum total_sales
niche_sales = df.groupby('product_niche')['total_sales'].sum().reset_index()
# display of the sales in each niche


# Group by product_niche and sum total_sales
niche_sales = df.groupby('product_niche')['total_sales'].sum().reset_index()
niche_sales = niche_sales.sort_values('total_sales', ascending=False)

plt.figure(figsize=(10,6))
bars = plt.bar(niche_sales['product_niche'], niche_sales['total_sales'], color='skyblue')
plt.xlabel('Product Niche')
plt.ylabel('Total Sales')
plt.title('Total Sales by Product Niche')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add sales count on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', 
             ha='center', va='bottom', fontsize=10)

# Group by product_niche and sum total_sales
niche_sales = df.groupby('product_details')['total_sales'].sum().reset_index()

# Find top 5 products by total quantity sold
top_products = df.groupby('product_details')['total_qty_sold'].sum().reset_index()
top_products = top_products.sort_values('total_qty_sold', ascending=False).head(5)
# Plot
plt.figure(figsize=(8,5))
bars = plt.bar(top_products['product_details'], top_products['total_qty_sold'], color='orange')
plt.xlabel('Product Details')
plt.ylabel('Total Quantity Sold')
plt.title('Top 5 Products by Quantity Sold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add quantity on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', 
             ha='center', va='bottom', fontsize=10)

# Calculate thresholds for classification
rms_high = df['relative_market_share'].quantile(0.66)
rms_low = df['relative_market_share'].quantile(0.33)
mg_high = df['market_growth'].quantile(0.66)
mg_low = df['market_growth'].quantile(0.33)

def classify(row):
    if row['relative_market_share'] >= rms_high and row['market_growth'] >= mg_high:
        return 'High'
    elif row['relative_market_share'] <= rms_low and row['market_growth'] <= mg_low:
        return 'Poor'
    else:
        return 'Average'

df['classification'] = df.apply(classify, axis=1)

# Display the classification for each product
print(df[['product_niche', 'product_id', 'product_details', 'relative_market_share', 'market_growth', 'classification']])