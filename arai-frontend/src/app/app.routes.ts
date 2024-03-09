import { Routes } from '@angular/router';
import { CaseInputComponent } from './case-input/case-input.component';
import { CostViewComponent } from './cost-view/cost-view.component';
import { MediatorsListComponent } from './mediators-list/mediators-list.component';

export const routes: Routes = [
    {
      path: '', // Explicit root path configuration
      redirectTo: '/input', // Redirect to '/input' as a default route
      pathMatch: 'full' // Ensures full match of the path
    },
    {
      path: '', // Base path for children
      children: [
        {path: 'input', component: CaseInputComponent},
        {path: 'koszt', component: CostViewComponent},
        {path: 'mediatorzy', component: MediatorsListComponent},
        {path: '**', component: CaseInputComponent} // Wildcard route for unmatched paths
      ]
    }
  ];
  
