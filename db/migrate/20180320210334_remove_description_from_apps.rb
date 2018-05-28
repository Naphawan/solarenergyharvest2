class RemoveDescriptionFromApps < ActiveRecord::Migration[5.1]
  def change
    remove_column :apps, :description, :string
  end
end
