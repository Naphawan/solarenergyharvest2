class AddCurrentToApps < ActiveRecord::Migration[5.1]
  def change
    add_column :apps, :Current, :float
  end
end
