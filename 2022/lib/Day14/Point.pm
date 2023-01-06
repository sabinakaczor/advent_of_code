package Day14::Point;

use v5.36;
use Moo;
use Mooish::AttributeBuilder;
use Types::Common;

# just a point - nothing to see here

has param 'x' => (
	isa => Types::Common::Int,
	writer => 1,
);

has param 'y' => (
	isa => Types::Common::Int,
	writer => 1,
);

sub clone_point ($self)
{
	return __PACKAGE__->new(x => $self->x, y => $self->y);
}

sub clone ($self)
{
	return $self->new(x => $self->x, y => $self->y);
}

1;

