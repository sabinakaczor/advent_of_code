use v5.36;

use lib 'local/lib/perl5';
use lib '2022/lib';

use autodie;

use Day14::Cave;
use Day14::Sand;

my $data = do {
	local $/ = undef;

	open my $fh, '<', '2022/input14.txt';
	scalar readline $fh;
};

my $cave = Day14::Cave->new(raw => $data);
my $sand = Day14::Sand->new(initial_pos => [500, 0], verbose => 0);
$sand->pour($cave);

say $sand->generation;

