import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pipescomp } from './pipescomp';

describe('Pipescomp', () => {
  let component: Pipescomp;
  let fixture: ComponentFixture<Pipescomp>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Pipescomp]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pipescomp);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
