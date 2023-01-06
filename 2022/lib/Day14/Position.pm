package Day14::Position;

use v5.36;
use Moo;
use Mooish::AttributeBuilder;
use Types::Common;

# This is an intelligent point which remembers where it felt
extends 'Day14::Point';

has field '_freefall_history' => (
	isa => Types::Common::ArrayRef,
	writer => 1,
	default => sub { [] },
);

sub clone ($self)
{
	my $clone = $self->SUPER::clone;
	$clone->_set_freefall_history($self->_freefall_history);

	return $clone;
}

sub backtrace ($self)
{
	my $last = pop $self->_freefall_history->@*;

	if ($last) {
		$self->set_x($last->x);
		$self->set_y($last->y);
		return !!1;
	}

	return !!0;
}

sub fallen ($self, $new_y = undef)
{
	$self->set_y($new_y) if defined $new_y;
	push $self->_freefall_history->@*, $self->clone_point;
}

sub possible_rolling_points ($self)
{
	my $this_x = $self->x;
	my $next_y = $self->y + 1;

	return (
		[$this_x - 1, $next_y],
		[$this_x + 1, $next_y],
	);
}

sub possible_falling_points ($self)
{
	my $this_x = $self->x;
	my $next_y = $self->y + 1;

	return (
		[$this_x, $next_y],
	);
}

sub as_string ($self)
{
	return sprintf "I'm a sand lump at %s,%s", $self->x, $self->y;
}

1;

