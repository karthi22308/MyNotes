import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Directivecomp } from './directivecomp';

describe('Directivecomp', () => {
  let component: Directivecomp;
  let fixture: ComponentFixture<Directivecomp>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Directivecomp]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Directivecomp);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
