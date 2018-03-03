class CreateApps < ActiveRecord::Migration[5.1]
  def change
    create_table :apps do |t|
      t.string :Firstname
      t.string :Lastname
      t.text :description

      t.timestamps
    end
  end
end
