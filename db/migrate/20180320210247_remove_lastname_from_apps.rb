class RemoveLastnameFromApps < ActiveRecord::Migration[5.1]
  def change
    remove_column :apps, :Lastname, :string
  end
end
