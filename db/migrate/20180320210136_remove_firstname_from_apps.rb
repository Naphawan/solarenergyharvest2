class RemoveFirstnameFromApps < ActiveRecord::Migration[5.1]
  def change
    remove_column :apps, :Firstname, :string
  end
end
