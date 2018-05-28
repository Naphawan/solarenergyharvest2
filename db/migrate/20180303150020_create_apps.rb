class CreateApps < ActiveRecord::Migration[5.1]
  def change
    create_table :apps do |t|
      t.string :mink
      t.string :Lastname
      t.text :description

      t.timestamps
    end
  end
end
