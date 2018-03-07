Rails.application.routes.draw do
  resources :apps

  get "control" => "apps#control"
  get "statistics" => "apps#statistics" 
  get "about" => "apps#about"
  get "index" => "apps#index" 

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
